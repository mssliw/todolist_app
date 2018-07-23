import pytest
import random

from mimesis import Generic
from random import randint
from sqlalchemy import event

from app import create_app
from app import db as _db

from models import TaskList, TaskCard, TaskDetails


g = Generic('en')


@pytest.fixture(scope="module")
def app():
    """
    Returns flask app with context for testing.
    """
    app = create_app()
    app.config['SERVER_NAME'] = 'example.com'
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client


@pytest.fixture(scope="module", autouse=True)
def db(app):
    """
    Returns module-wide initialised database.
    """
    _db.create_all()

    yield _db


@pytest.fixture(scope="module")
def session(db):
    """
    Returns module-scoped session.
    """
    conn = db.engine.connect()
    txn = conn.begin()

    options = dict(bind=conn, binds={})
    sess = db.create_scoped_session(options=options)

    sess.begin_nested()

    @event.listens_for(sess(), 'after_transaction_end')
    def restart_savepoint(sess2, trans):
        if trans.nested and not trans._parent.nested:
            sess2.expire_all()
            sess.begin_nested()

    db.session = sess
    yield sess

    sess.remove()
    txn.rollback()
    conn.close()


@pytest.fixture(scope="function")
def db_task_list(session, client):
    """
    Creates and returns function-scoped database entry for task list
    """
    task_list = TaskList(
        id=randint(1, 30),
        list_title=' '.join(g.text.title().split(' ')[:5])
    )

    yield (task_list)


@pytest.fixture(scope="function")
def db_task_card(session, client, db_task_list):
    """
    Creates and returns function-scoped database entry for task card
    """
    task_card = TaskCard(
        id=randint(1, 30),
        card_title=' '.join(g.text.title().split(' ')[:5]),
        task_list_id=db_task_list.id,
    )

    yield (task_card)


@pytest.fixture(scope="function")
def db_task_details(session, client, db_task_card):
    """
    Creates and returns function-scoped database entry for task details
    """
    task_details = TaskDetails(
        id=randint(1, 30),
        task_description=g.text.sentence(),
        task_card_id=db_task_card.id,
    )

    yield (task_details)

