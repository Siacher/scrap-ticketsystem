from flask import Blueprint, render_template, redirect, url_for, flash, request

from src.forms import ManageStatusForm
from src.routes.api import db

index_route = Blueprint('status', __name__)


@index_route.route('/manage_status', methods=['GET', 'POST'])
def manage_status():
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM status"
        cursor.execute(sql)

        status = cursor.fetchall()

        form = ManageStatusForm()


        if form.submit.data and form.is_submitted():
            sql = "INSERT INTO status(text, completion, color) VALUES (%s, %s, %s)"
            cursor.execute(sql, (form.text.data, form.completion.data, str(form.color.data)))
            return redirect(url_for('status.manage_status'))

        if request.method == 'POST' and request.form['delete']:
            status_id = request.form['delete']
            sql = "DELETE FROM status WHERE id = %s"
            cursor.execute(sql, (status_id,))
            return redirect(url_for('status.manage_status'))

        db.connection.commit()

    return render_template('manage_status.html', form=form, status=status, subsite=True)
