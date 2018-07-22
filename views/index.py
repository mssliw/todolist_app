from flask import Blueprint, redirect, render_template, request, url_for

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
    return render_template('index.html', incomplete=incomplete, accomplished=accomplished, task_descriptions=task_descriptions, task_lists=task_lists, lists_accomplished=list_accomplished)


@todolist.route('/create_new_list', methods=['POST'])
def create_new_list():
    list_title = request.form['create-new-list']
    all_lists = db.session.query(TaskList).all()
    titles = [list.list_title for list in all_lists]
    if list_title and list_title not in titles:
        new_list = TaskList(list_title=request.form['create-new-list'])
        db.session.add(new_list)
        db.session.commit()
    elif not list_title:
        print('Name of the list cannot be empty')
    elif list_title in titles:
        print('Name of the list should be unique')
    else:
        print('Something went wrong')
    return redirect(url_for('todolist.index'))


@todolist.route('/add/<list_title>', methods=['POST'])
def add(list_title):
    task_list = TaskList.query.filter_by(list_title=list_title).first()
    new_task = TaskCard(card_title=request.form['task-to-do'], accomplished=False, task_list=task_list)
    task_list.newly_created = False;
    db.session.add(new_task)
    db.session.commit()

    detail = TaskDetails(task_description=request.form['details-to-do'], task_card_id=new_task.id)
    db.session.add(detail)
    db.session.commit()

    return redirect(url_for('todolist.index'))


@todolist.route('/update', methods=['POST'])
def update():
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
