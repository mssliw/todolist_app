from flask import url_for


def test_app_response(client):
    resp = client.get(url_for("todolist.index"))
    assert resp.status_code == 200


