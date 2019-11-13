from flask import Flask

# public routes
from src.routes.public.index import index_route

# api routes
from src.routes.api.label import label_route
from src.routes.api.category import category_route
from src.routes.api.prio import prio_route
from src.routes.api.status import status_route


class ScrapTicketSystem:
    def __init__(self):
        self.app = Flask(__name__)

        # public routes
        self.app.register_blueprint(index_route)

        # api routes
        self.app.register_blueprint(label_route, url_prefix="/api/v1")
        self.app.register_blueprint(category_route, url_prefix="/api/v1")
        self.app.register_blueprint(prio_route, url_prefix="/api/v1")
        self.app.register_blueprint(status_route, url_prefix="/api/v1")

    def run(self):
        self.app.run(port=3000)