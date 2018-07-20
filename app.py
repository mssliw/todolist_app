from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/magda/PycharmProjects/todolist_app/data/todolist.db"

db = SQLAlchemy(app)


class TaskList(db.Model):
    __tablename__ = "task-list"
    id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(db.String(256),
                           nullable=False)
    list_accomplished = db.Column(db.Boolean)

    task_cards = db.relationship('TaskCard')


class TaskCard(db.Model):
    __tablename__ = "task-card"
    id = db.Column(db.Integer, primary_key=True)
    card_title = db.Column(db.String(256))
    accomplished = db.Column(db.Boolean)

    task_list_id = db.Column(db.Integer,
                             db.ForeignKey('task-list.id'),
                             nullable=False)
    task_list = db.relationship('TaskList',
                                back_populates='task_cards')
    task_details = db.relationship('TaskDetails')


class TaskDetails(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    task_description = db.Column(db.String(512))

    task_card_id = db.Column(db.Integer,
                             db.ForeignKey('task-card.id'),
                             nullable=False)
    task_card = db.relationship('TaskCard',
                                back_populates='task_details')


@app.route('/')
def index():
    task_lists = db.session.query(TaskList).all()
    incomplete = TaskCard.query.filter_by(accomplished=False).all()
    accomplished = TaskCard.query.filter_by(accomplished=True).all()
    list_accomplished = TaskCard.query.filter_by(accomplished=False).all()
    task_descriptions = db.session.query(TaskDetails).all()
    print(task_descriptions, task_lists)
    return render_template('index.html', incomplete=incomplete, accomplished=accomplished, task_descriptions=task_descriptions, task_lists=task_lists, lists_accomplished=list_accomplished)


@app.route('/create_new_list', methods=['POST'])
def create_new_list():
    new_list = TaskList(list_title=request.form['create-new-list'])
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add/<list_title>', methods=['POST'])
def add(list_title):
    task_list = TaskList.query.filter_by(list_title=list_title).first()
    # task_list = db.session.query(TaskList).first()
    new_task = TaskCard(card_title=request.form['task-to-do'], accomplished=False, task_list=task_list)
    db.session.add(new_task)
    db.session.commit()

    detail = TaskDetails(task_description=request.form['details-to-do'], task_card_id=new_task.id)
    db.session.add(detail)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    return redirect(url_for('index'))


@app.route('/accomplished/<id>')
def complete(id):
    task_list = TaskCard.query.filter_by(id=int(id)).first().task_list
    task = TaskCard.query.filter_by(id=int(id)).first()
    task.accomplished = True
    db.session.commit()
    still_to_do = TaskCard.query.filter_by(accomplished=False).first()
    if not still_to_do:
        task_list.accomplished = True
        db.session.commit()

    return redirect(url_for('index'))


# @app.route('/details/<id>')
# def details(id):
#     details_id = TaskDetails.query.filter_by(task_card_id=int(id))
#
#     return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
