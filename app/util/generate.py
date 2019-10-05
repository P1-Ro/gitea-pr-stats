from app import db
from app.util import prst
import config


def generate(repo_name, from_date=None, to_date=None):
    stats = prst.PrSt(config.username, config.password,
                      repo_name, from_date, to_date)

    table = db.table("report")

    stats.result["name"] = repo_name
    stats.result["id"] = table._last_id + 1

    table.insert(stats.result)
