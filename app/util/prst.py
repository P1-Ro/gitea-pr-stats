import collections

import requests
import time

import config
from app.util import patch

base = config.gite_url + "/api/v1"


class PrSt(object):

    def __init__(self, username, password, repo_name, sprint_start=None, sprint_end=None):
        self.gh = requests.Session()
        self.gh.auth = (username, password)
        self.repo_name = repo_name
        self.sprint_start = sprint_start
        self.sprint_end = sprint_end
        self.result = {}
        self.loaded = []

        self.user_stats = collections.defaultdict(
            lambda: collections.defaultdict(int))
        self.opened_prs = []
        self.merged_prs = []
        self.pull_stats = collections.defaultdict(
            lambda: collections.defaultdict(int))

        self.compute()

    def load_all(self, url):
        params = {
            "page": 1,
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
            "state": "all",
        }
        while True:
            r = self.gh.get(url, params=params)
            body = r.json()
            if len(body) > 0:
                res_id = body[0].get("id") if isinstance(body, list) else body.get("id")
                if res_id in self.loaded:
                    break
                self.loaded.append(res_id)
                for pr in body:
                    yield pr
                params["page"] += 1
            else:
                break

    def load_prs(self):
        return self.load_all("%s/repos/%s/pulls" % (base, self.repo_name))

    def load_comments(self, pr_number):
        return self.load_all("%s/repos/%s/issues/%d/comments" %
                             (base, self.repo_name, pr_number))

    def take_in_sprint(self, xs):
        for x in xs:
            updated = x.get("updated_at", x.get("created_at", None))
            if self.in_sprint(updated):
                yield x
            else:
                break

    def in_sprint(self, x):
        if x is None:
            return False
        if self.sprint_start is None or self.sprint_end is None:
            return True
        return self.sprint_start < x < self.sprint_end

    def compute(self):
        prs = self.take_in_sprint(self.load_prs())
        for pr in prs:
            print(pr)
            if self.in_sprint(pr["created_at"]):
                self.user_stats[pr["user"]["login"]]["opened-prs"] += 1
                self.opened_prs.append(pr["number"])
                if pr["title"].lower().startswith("hot-fix"):
                    self.user_stats[pr["user"]["login"]]["hot-fix"] += 1
            if self.in_sprint(pr["created_at"]) or self.in_sprint(pr["merged_at"]):
                res = self.gh.get("%s/repos/%s/pulls/%d" %
                                  (base, self.repo_name, pr["number"]))
                pr = res.json()
                self.pull_stats[pr["number"]]["opener"] = pr["user"]["login"]
            users = set()
            comments = self.take_in_sprint(self.load_comments(pr["number"]))
            for comment in comments:
                login = comment["user"]["login"]
                self.user_stats[login]["comments"] += 1
                users.add(login)
            for user in users:
                self.user_stats[user]["commented-on-prs"] += 1

            diff_url = pr["diff_url"]
            p = patch.fromstring(self.gh.get(diff_url).content)
            files, adds, deletes = p.diffstat()

            self.pull_stats[pr["number"]]["additions"] = adds
            self.pull_stats[pr["number"]]["deletions"] = deletes
            self.pull_stats[pr["number"]]["changed_files"] = files

            if self.in_sprint(pr["merged_at"]):
                login = pr["user"]["login"]
                self.merged_prs.append(pr["number"])
                self.user_stats[login]["merged_additions"] += adds
                self.user_stats[login]["merged_deletions"] += deletes
                self.user_stats[login]["merged_changed_files"] += files

                merger = pr["merged_by"]["login"]
                self.user_stats[merger]["merged"] += 1

        for pr_num in self.pull_stats:
            for prop in ["additions", "deletions", "changed_files"]:
                pr = self.pull_stats[pr_num]
                login = pr.get("opener", None)
                if login is None:
                    continue
                self.user_stats[login]["opened_" + prop] += pr[prop]

        for key in self.user_stats:
            self.user_stats[key]["name"] = key

        self.result = {
            "users": list(self.user_stats.values()),
            "timespan": {
                "start": self.sprint_start,
                "end": self.sprint_end,
                "captured_at": int(time.time()) * 1000,
            },
        }
