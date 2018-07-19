from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/magda/PycharmProjects/todolist_app/todolist.db"

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    completed = db.Column(db.Boolean)


@app.route('/')
def index():
    incomplete = Todo.query.filter_by(completed=False).all()
    complete = Todo.query.filter_by(completed=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['item-to-do'], completed=False)
    db.session.add(todo)
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


if __name__ == "__main__":
    app.run(debug=True)
