from flask import abort, Blueprint, redirect, render_template, request, url_for

from forms.forms import CreateListForm, AddCardForm, AddDetailsForm
from init_db import db
from models.task_lists import (TaskList, TaskCard, TaskDetails)


todolist = Blueprint('todolist', __name__,
                     template_folder='templates')


@todolist.route('/')
def index():
    task_lists = db.session.query(TaskList).all()
    incomplete = TaskCard.query.filter_by(accomplished=False).all()
    accomplished = TaskCard.query.filter_by(accomplished=True).all()
    list_accomplished = TaskCard.query.filter_by(accomplished=False).all()
    task_descriptions = db.session.query(TaskDetails).all()
    create_list_form = CreateListForm()
    add_card_form = AddCardForm()
    add_details_form = AddDetailsForm()
    return render_template('index.html', incomplete=incomplete, accomplished=accomplished, task_descriptions=task_descriptions, task_lists=task_lists, lists_accomplished=list_accomplished,
                           create_list_form=create_list_form, add_card_form=add_card_form, add_details_form=add_details_form)


@todolist.route('/create_new_list', methods=['POST'])
def create_new_list():
    # list_title = request.form['create-new-list']
    # all_lists = db.session.query(TaskList).all()
    # titles = [list.list_title for list in all_lists]
    # if list_title and list_title not in titles:
    #     new_list = TaskList(list_title=request.form['create-new-list'])
    #     db.session.add(new_list)
    #     db.session.commit()
    # elif not list_title:
    #     print('Name of the list cannot be empty')
    # elif list_title in titles:
    #     print('Name of the list should be unique')
    # else:
    #     print('Something went wrong')

    create_list_form = CreateListForm()
    if create_list_form.validate_on_submit():
        try:
            new_list = TaskList(list_title=create_list_form.list_title.data)
            db.session.add(new_list)
            db.session.commit()
        except Exception:
            abort(500)
    return redirect(url_for('todolist.index'))


@todolist.route('/add/<list_title>', methods=['POST'])
def add(list_title):
    # task_list = TaskList.query.filter_by(list_title=list_title).first()
    # new_task = TaskCard(card_title=request.form['task-to-do'], accomplished=False, task_list=task_list)
    # task_list.newly_created = False
    # db.session.add(new_task)
    # db.session.commit()
    #
    # detail = TaskDetails(task_description=request.form['details-to-do'], task_card_id=new_task.id)
    # db.session.add(detail)
    # db.session.commit()


    add_card_form = AddCardForm()
    if add_card_form.validate_on_submit():
        try:
            task_list = TaskList.query.filter_by(list_title=list_title).first()
            task_list.newly_created = False
            new_card = TaskCard(card_title=add_card_form.card_title.data, accomplished=False, task_list=task_list)
            db.session.add(new_card)
            db.session.commit()
        except Exception:
            abort(500)
    return redirect(url_for('todolist.index'))


@todolist.route('/add_details/<id>', methods=['POST'])
def add_details(id):
    add_details_form = AddDetailsForm()
    if add_details_form.validate_on_submit():
        try:
            task_card = TaskCard.query.filter_by(id=id).first()
            new_detail = TaskDetails(task_description=add_details_form.task_description.data, task_card=task_card)
            db.session.add(new_detail)
            db.session.commit()
        except Exception:
            print('wtf')
    return redirect(url_for('todolist.index'))


@todolist.route('/accomplished/<id>')
def complete(id):
    task_list = TaskCard.query.filter_by(id=int(id)).first().task_list
    task = TaskCard.query.filter_by(id=int(id)).first()
    task.accomplished = True
    db.session.commit()
    still_to_do = TaskCard.query.filter_by(accomplished=False).first()
    if not still_to_do:
        task_list.accomplished = True
        db.session.commit()

    return redirect(url_for('todolist.index'))


@todolist.route('/remove/<id>')
def remove(id):
    task_list = TaskList.query.filter_by(id=int(id)).first()
    tasks_at_list = task_list.task_cards
    [[db.session.delete(detail) for detail in task.task_details] for task in tasks_at_list]
    [db.session.delete(task) for task in tasks_at_list]
    db.session.delete(task_list)
    db.session.commit()

    return redirect(url_for('todolist.index'))
