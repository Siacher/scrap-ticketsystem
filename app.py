#!/usr/bin/python
"""Main File to run application"""

from flask import Flask
from src.routes.label import label_route


class ScrapTicketSystem:
    def __init__(self):
        app = Flask(__name__)
        app.register_blueprint(label_route, url_prefix="/api/v1")

        app.run(port=3000)


if __name__ == "__main__":
    ScrapTicketSystem()
