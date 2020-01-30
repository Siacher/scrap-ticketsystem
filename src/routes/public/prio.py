from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.routes.api import db

from src.forms import ManagePrioForm

index_route = Blueprint('prio', __name__)


@index_route.route('/manage_prio', methods=['GET', 'POST'])
def manage_prio():
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM prio"
        cursor.execute(sql)

        prio = cursor.fetchall()

        form = ManagePrioForm()
        if form.submit.data and form.is_submitted():
            print(form.color.data)
            sql = "INSERT INTO prio(text, prio, color) VALUES (%s, %s, %s)"
            cursor.execute(sql, (form.text.data, form.prio.data, str(form.color.data)))
            return redirect(url_for('prio.manage_prio'))

        if request.method == 'POST' and request.form['delete']:
            prio_id = request.form['delete']
            sql = "DELETE FROM prio WHERE id = %s"
            cursor.execute(sql, (prio_id,))
            return redirect(url_for('prio.manage_prio'))

        db.connection.commit()

    return render_template('manage_prio.html', form=form, prio=prio, subsite=True)
