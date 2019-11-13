from flask import Blueprint, render_template

index_route = Blueprint('index', __name__)


@index_route.route('/', methods=['GET'])
def index():
    return render_template('index.html')
