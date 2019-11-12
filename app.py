#!/usr/bin/python
"""Main File to run application"""

from flask import Flask
from src.routes.label import label_route
from src.routes.category import category_route
from src.routes.prio import prio_route
from src.routes.status import status_route


class ScrapTicketSystem:
    def __init__(self):
        app = Flask(__name__)
        app.register_blueprint(label_route, url_prefix="/api/v1")
        app.register_blueprint(category_route, url_prefix="/api/v1")
        app.register_blueprint(prio_route, url_prefix="/api/v1")
        app.register_blueprint(status_route, url_prefix="/api/v1")

        app.run(port=3000)


if __name__ == "__main__":
    ScrapTicketSystem()
