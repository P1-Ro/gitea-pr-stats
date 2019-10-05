from flask import request
from flask_restplus import Resource
from tinydb import Query, where

import config
from app import db
from app.util import generate
from . import api_rest


@api_rest.route('/repos/all')
class Repos(Resource):

    def get(self):
        return config.repositories


@api_rest.route('/report/<string:resource_id>')
class Report(Resource):

    def get(self, resource_id):
        table = db.table("report")
        if resource_id == "all":
            reports = table.all()
            for curr in reports:
                curr.pop("users", None)
                curr["name"] = curr["name"].split("/")[1]
            return sorted(reports, key=lambda x: x["timespan"]["captured_at"], reverse=True)

        q = Query()
        return table.search(q.id == int(resource_id))[0]

    def delete(self, resource_id):
        table = db.table("report")
        return 200 if len(table.remove(where("id") == int(resource_id))) != 0 else 500


@api_rest.route('/generate')
class Generate(Resource):

    def post(self):
        json_payload = request.json
        return generate.generate(json_payload["project"], json_payload["from"], json_payload["to"])
