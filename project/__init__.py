from flask import Flask

from project.views import init_views


def create_app():
    app = Flask(__name__)

    init_views(app)

    return app