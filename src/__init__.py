from flask import Flask
from flask_assets import Bundle, Environment

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
from src.routes.api.ticket import ticket_route


class ScrapTicketSystem:
    def __init__(self):

        # init app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

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
        self.app.register_blueprint(ticket_route, url_prefix="/api/v1")

        # assets
        bundles = {

            'create_js': Bundle(
                'js/common.js',
                'js/create_ticket.js',
                'js/create_category.js',
                output='gen/create.js',
                filters='jsmin'),

            'common_js': Bundle(
                'js/common.js',
                output='gen/create.js',
                filters='jsmin'),

            'start_js': Bundle(
                'js/start.js',
                output='gen/start.js',
                filters='jsmin')
        }

        assets = Environment(self.app)
        assets.debug = True
        assets.init_app(self.app)

        assets.register(bundles)

    def run(self):
        self.app.run(port=3000)