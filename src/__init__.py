from flask import Flask
from flask_login import LoginManager

# public routes
from src.routes.public.index import index_route

# api routes
from src.routes.api.label import label_route
from src.routes.api.category import category_route
from src.routes.api.prio import prio_route
from src.routes.api.status import status_route
from src.routes.api.user import user_route
from src.routes.api.company import company_route
from src.routes.api.comment import comment_route


class ScrapTicketSystem:
    def __init__(self):

        # init app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
        self.login_manager = LoginManager(self.app)

        # public routes
        self.app.register_blueprint(index_route)

        # api routes
        self.app.register_blueprint(label_route, url_prefix="/api/v1")
        self.app.register_blueprint(category_route, url_prefix="/api/v1")
        self.app.register_blueprint(prio_route, url_prefix="/api/v1")
        self.app.register_blueprint(status_route, url_prefix="/api/v1")
        self.app.register_blueprint(user_route, url_prefix="/api/v1")
        self.app.register_blueprint(company_route, url_prefix="/api/v1")
        self.app.register_blueprint(comment_route, url_prefix="/api/v1")

    def run(self):
        self.app.run(port=3000)