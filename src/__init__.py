from flask import Flask
from flask_assets import Bundle, Environment
from flask_login import LoginManager

# public routes
from src.routes.public.index import index_route
from src.routes.public.ticket import index_route as ticket_route
from src.routes.public.category import index_route as category_route
from src.routes.public.prio import index_route as prio_route
from src.routes.public.status import index_route as status_route
from src.routes.public.user import index_route as user_route


from src.routes.public import login

# init app
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

# public routes
app.register_blueprint(index_route)
app.register_blueprint(ticket_route)
app.register_blueprint(category_route)
app.register_blueprint(prio_route)
app.register_blueprint(status_route)
app.register_blueprint(user_route)

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
        filters='jsmin'),

    'manage_user_js': Bundle(
        'js/common.js',
        'js/manageUser.js',
        output='gen/start.js',),

}

assets = Environment(app)
assets.debug = False



assets.init_app(app)
assets.register(bundles)

login.init_app(app)


