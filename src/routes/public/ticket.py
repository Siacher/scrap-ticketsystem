from datetime import datetime
from sqlite3 import IntegrityError

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from src.routes.api import db

from src.forms import CreateTicketForm, CreateCommentForm, UpdateTicketForm

from src.shared.choiceSort import choice_sort

index_route = Blueprint('ticket', __name__)


@index_route.route('/ticket/<_id>', methods=['GET', 'POST'])
def ticket(_id):
    with db.connection.cursor() as cursor:
        sql = "SELECT t.header as header, t.text as text, p.text as prio, p.color as prio_color, c.text as category, s.text as status, s.color as status_color FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id LEFT JOIN status as s on t.status_id = s.id WHERE t.id = %s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()

    form = CreateCommentForm()
    if form.is_submitted() and form.submit.data:
        header = form.header.data
        text = form.text.data
        created_at = datetime.datetime.now()
        created_by = current_user.id
        ticket_id = _id

        with db.connection.cursor() as cursor:
            sql = "INSERT INTO comment(header, text, created_at, created_by, ticket_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (header, text, created_at, created_by, ticket_id))
        db.connection.commit()
        comments = db.get_all_join_ticket_id(ticket_id)
        return redirect(url_for('ticket.ticket', _id=_id))

    comments = db.get_all_join_ticket_id(_id)
    return render_template('ticket.html', ticket=result, form=form, comments=comments, subsite=True, _ticket=_id)


@index_route.route('/ticket/<_id>/update', methods=['GET', 'POST'])
def update_ticket(_id):
    with db.connection.cursor() as cursor:
        sql = "SELECT t.header as header, t.text as text, p.text as prio, p.color as prio_color, c.text as category, s.text as status, s.color as status_color FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id LEFT JOIN status as s on t.status_id = s.id WHERE t.id = %s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()

    prio_return = db.get_all("prio")
    prio = [i['text'] for i in prio_return]
    _prio = choice_sort(prio, result['prio'])

    category_return = db.get_all("category")
    category = [i['text'] for i in category_return]
    _category = choice_sort(category, result['category'])

    user_return = db.get_all("user")
    user = [(i['id'], f"{i['first_name']} {i['last_name']} | {i['email']}") for i in user_return]

    status_return = db.get_all("status")
    status = [i['text'] for i in status_return]
    _status = choice_sort(status, result['status'])

    form = UpdateTicketForm()
    form.prio.choices = _prio
    form.category.choices = _category
    form.status.choices = _status
    form.user.choices = user

    form.header.data = result["header"]
    form.text.data = result["text"]

    if form.is_submitted():
        header = form.header.data
        text = form.text.data
        user_id = form.user.data
        with db.connection.cursor() as cursor:
            sql = "SELECT id FROM prio WHERE text = %s"
            cursor.execute(sql, (form.prio.choices[int(form.prio.data)][1],))
            prio_id = cursor.fetchone()['id']

            sql = "SELECT id FROM status WHERE text = %s"
            cursor.execute(sql, (form.status.choices[int(form.status.data)][1],))
            status_id = cursor.fetchone()['id']

            sql = "SELECT id FROM category WHERE text = %s"
            cursor.execute(sql, (form.category.choices[int(form.category.data)][1],))
            category_id = cursor.fetchone()['id']
            try:
                sql = "UPDATE ticket set header = %s, text = %s,  category_id = %s, prio_id= %s, status_id= %s, assign_to= %s  WHERE ticket.id = %s "
                cursor.execute(sql, (header, text, category_id, prio_id, status_id, user_id, _id))
            except IntegrityError as ConstraintError:
                flash("Kann nicht gelöscht werden. Wird noch verwendet")
            finally:
                return redirect(url_for('index.index'))
    db.connection.commit()

    return render_template('update_ticket.html', form=form, subsite=True)


@index_route.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    prio_return = db.get_all("prio")
    prio = [(i['id'], i['text']) for i in prio_return]

    category_return = db.get_all("category")
    category = [(i['id'], i['text']) for i in category_return]

    status_return = db.get_all("status")
    status = [(i['id'], i['text']) for i in status_return]

    form = CreateTicketForm()
    form.prio.choices = prio
    form.category.choices = category
    form.status.choices = status

    if form.is_submitted():
        header = form.header.data
        text = form.text.data
        prio_id = form.prio.data
        category_id = form.category.data
        status_id = form.status.data
        user_id = current_user.id

        with db.connection.cursor() as cursor:
            sql = "INSERT INTO ticket(header, text,  category_id, prio_id, status_id, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (header, text, category_id, prio_id, status_id, user_id))
        db.connection.commit()
        return redirect(url_for('index.index'))

    return render_template('create_ticket.html', form=form, subsite=True)


@index_route.route('/kanban', methods=['GET', 'POST'])
def kanban():
    with db.connection.cursor() as cursor:
        sql = "SELECT id, text, color FROM status ORDER BY completion"
        cursor.execute(sql)
        status = cursor.fetchall()

        for stat in status:
            sql = "SELECT header, ticket.id, c.email, a.email FROM ticket LEFT JOIN user as c ON ticket.created_by = c.id LEFT JOIN user as a ON ticket.assign_to = a.id WHERE status_id = %s"
            cursor.execute(sql, (stat['id'],))
            stat['tickets'] = cursor.fetchall()

    return render_template('kanban.html', subsite=True, status=status)