import os
from flask import Flask, current_app, send_file
from tinydb import TinyDB

db = TinyDB('db.json')
app = Flask(__name__, static_folder='../client/dist')

from .api import api_bp  # NOQA
app.register_blueprint(api_bp)

from .config import Config  # NOQA

app.logger.info('>>> {}'.format(Config.FLASK_ENV))


@app.route('/')
@app.route('/<path:path>')
def index_client(path="index.html"):
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, path)
    return send_file(entry)


