from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/magda/PycharmProjects/todolist_app/data/todolist.db"

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    completed = db.Column(db.Boolean)
    # details_id = db.Column(db.Integer, db.ForeignKey("details.id"))


class Details(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))

    todo_id = db.Column(db.Integer,
                        db.ForeignKey('todo.id'),
                        nullable=False)
    todo = db.relationship('Todo',
                           foreign_keys=todo_id)


@app.route('/')
def index():
    incomplete = Todo.query.filter_by(completed=False).all()
    complete = Todo.query.filter_by(completed=True).all()
    details = None
    for i in incomplete:
        details = Details.query.filter_by(todo_id=i.id).first()
    #     print(i.id, details.text, "for loop")
    # print(incomplete, details.text, 'after for loop')
    return render_template('index.html', incomplete=incomplete, complete=complete, details=details)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['item-to-do'], completed=False)
    db.session.add(todo)
    db.session.commit()

    detail = Details(text=request.form['details-to-do'], todo_id=todo.id)
    db.session.add(detail)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.completed = True
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/details/<id>')
def details(id):
    details = Details.query.filter_by(id=int(id).first())
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
