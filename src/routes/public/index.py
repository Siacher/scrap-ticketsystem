from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from src.routes.api import db


from jinja2 import Environment as Jinja2Environment
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension
from scss import Compiler

assets_env = AssetsEnvironment('./static', '/')
jinja2_env = Jinja2Environment(extensions=[AssetsExtension])
jinja2_env.assets_environment = assets_env

index_route = Blueprint('index', __name__)


@index_route.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    else:
        with db.connection.cursor() as cursor:
            sql = "SELECT ug.name, ug.id FROM user_group as ug JOIN user_in_group uig on ug.id = uig.group_id JOIN user u on uig.user_id = u.id WHERE u.id = %s"
            cursor.execute(sql, (current_user.id,))
            group = cursor.fetchone()

            user_group = 'default'
            try:
                if group['name']:
                    user_group = group['name']
            except TypeError as NOUSERGROUP:
                print(NOUSERGROUP)

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.created_by = %s"
            cursor.execute(sql, (current_user.id,))
            my_tickets = cursor.fetchall()

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.assign_to = %s"
            cursor.execute(sql, (current_user.id,))
            ass_tickets = cursor.fetchall()

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.assign_to = NULL AND t.created_by != %s"
            cursor.execute(sql, (current_user.id,))
            not_ass_tickets = cursor.fetchall()

    return render_template('index.html', my_tickets=my_tickets, ass_tickets=ass_tickets,
                           not_ass_tickets=not_ass_tickets, user_group=user_group)
