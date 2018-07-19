from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/magda/PycharmProjects/todolist_app/data/todolist.db"

db = SQLAlchemy(app)


class TaskList(db.Model):
    __tablename__ = "task-list"
    id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(db.String(256))


class TaskCard(db.Model):
    __tablename__ = "task-card"
    id = db.Column(db.Integer, primary_key=True)
    card_title = db.Column(db.String(256))
    accomplished = db.Column(db.Boolean)

    task_list_id = db.Column(db.Integer,
                             db.ForeignKey('task-list.id'))
    task_list = db.relationship('TaskList',
                                foreign_keys=task_list_id)


class TaskDetails(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    task_description = db.Column(db.String(512))

    task_card_id = db.Column(db.Integer,
                             db.ForeignKey('task-card.id'))
    task_card = db.relationship('TaskCard',
                                foreign_keys=task_card_id)


@app.route('/')
def index():
    incomplete = TaskCard.query.filter_by(accomplished=False).all()
    accomplished = TaskCard.query.filter_by(accomplished=True).all()
    task_details = [TaskDetails.query.filter_by(task_card_id=i.id).first().task_description for i in incomplete if not None]
    print(task_details)
    #FIXME: push parameters of one detail properly
    return render_template('index.html', incomplete=incomplete, accomplished=accomplished, task_details=task_details)


@app.route('/add', methods=['POST'])
def add():
    new_task = TaskCard(card_title=request.form['item-to-do'], accomplished=False)
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
    task = TaskCard.query.filter_by(id=int(id)).first()
    task.accomplished = True
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/details/<id>')
def details(id):
    details_id = TaskDetails.query.filter_by(task_card_id=int(id))

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
