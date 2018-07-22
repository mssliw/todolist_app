from init_db import db


class TaskList(db.Model):
    __tablename__ = "task-list"
    id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(db.String(256),
                           unique=True,
                           nullable=False)
    newly_created = db.Column(db.Boolean,
                              default=True)
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
