import pytest

from mimesis import Generic
from random import randint
from sqlalchemy import event

from app import create_app
from app import db as _db

from forms.forms import CreateListForm, AddCardForm, AddDetailsForm

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
def db_tasks(session, client):
    """
    Creates and returns function-scoped database entry for task list
    """
    task_list = TaskList(
        id=randint(1000, 30000),
        list_title=' '.join(g.text.title().split(' ')[:5])
    )

    task_card = TaskCard(
        id=randint(1000, 30000),
        card_title=' '.join(g.text.title().split(' ')[:5]),
        accomplished=False,
        task_list_id=task_list.id
    )

    task_details = TaskDetails(
        id=randint(1000, 30000),
        task_description=g.text.sentence(),
        task_card_id=task_card.id
    )
    yield (task_list, task_card, task_details)


@pytest.fixture(scope="function")
def add_list_form(session, client):
    add_form = CreateListForm(
        id=randint(1, 30),
        list_title=' '.join(g.text.title().split(' ')[:5]),
        newly_created=True,
    )

    yield (add_form)


@pytest.fixture(scope="function")
def add_card_form(session, client, db_tasks):
    add_form = AddCardForm(
        id=randint(1, 30),
        card_title=' '.join(g.text.title().split(' ')[:5]),
        accomplished=False,
        task_list_id=db_tasks[0].id,
        list_title=db_tasks[0].list_title
    )
    yield (add_form)


@pytest.fixture(scope="function")
def add_details_form(session, client, db_tasks):
    task_card_id = db_tasks[1].task_details
    add_form = AddDetailsForm(
        id=randint(1, 30),
        task_description=' '.join(g.text.sentence().split(' ')[:5]),
        task_card_id=task_card_id
    )
    yield (add_form)
