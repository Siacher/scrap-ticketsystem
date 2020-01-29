from flask import Blueprint, render_template, redirect, url_for, flash, request

from src.forms import ManageCategroyForm
from src.routes.api import db

index_route = Blueprint('category', __name__)


@index_route.route('/manage_category', methods=['GET', 'POST'])
def manage_category():
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM category"
        cursor.execute(sql)

        categories = cursor.fetchall()

        form = ManageCategroyForm()
        if form.submit.data and form.is_submitted():
            sql = "INSERT INTO category(text) VALUES (%s)"
            cursor.execute(sql, (form.text.data,))
            return redirect(url_for('category.manage_category'))

        if request.method == 'POST' and request.form['delete']:
            cat_id = request.form['delete']
            sql = "DELETE FROM category WHERE id = %s"
            cursor.execute(sql, (cat_id,))
            return redirect(url_for('category.manage_category'))

        db.connection.commit()

    return render_template('manage_category.html', form=form, categories=categories, subsite=True)
