from flask import url_for

from models import TaskList, TaskCard, TaskDetails


def test_app_response(client):
    resp = client.get(url_for("todolist.index"))
    assert resp.status_code == 200


def test_create_new_list_response(client):
    resp = client.post(url_for("todolist.create_new_list"))
    assert resp.status_code == 302


def test_add_task_list_card_detail(session, db_tasks):
    try:
        task_list = db_tasks[0]
        task_lists_before = TaskList.query.count()
        session.add(task_list)
        session.commit()
        task_list_after = TaskList.query.count()

        task_cards_before = TaskCard.query.count()
        task_card = db_tasks[1]
        session.add(task_card)
        session.commit()
        task_cards_after = TaskCard.query.count()

        task_details_before = TaskDetails.query.count()
        task_details = db_tasks[2]
        session.add(task_details)
        session.commit()
        task_details_after = TaskDetails.query.count()
    except:
        session.rollback()
        raise
    assert (task_list_after - task_lists_before) == 1

    assert (task_cards_after - task_cards_before) == 1

    assert (task_details_after - task_details_before) == 1
