import os
from flask import Flask

from init_db import db
from views.index import todolist


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///home/magda/PycharmProjects/todolist_app/data/todolist.db"
    # POSTGRES = {
    #     'user': 'postgres',
    #     'pw': 'password',
    #     'db': 'todolist',
    #     'host': 'localhost',
    #     'port': '5432',
    # }
    #
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(todolist)
    app.secret_key = os.urandom(24)

    db.init_app(app)

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
