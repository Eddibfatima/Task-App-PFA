from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import abort
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    job = db.Column(db.String(20))
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    picture = db.Column(db.LargeBinary())
    mimetype = db.Column(db.Text)
    filename = db.Column(db.Text)
    task = db.relationship('Task', backref='user', passive_deletes=True)
    comment = db.relationship('Comment', backref='user', passive_deletes=True)


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    open_task = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    ongoing_task = db.Column(db.String(20), nullable=True)
    task_descriptif = db.Column(db.String(200), nullable=False)
    operator = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    finished = db.relationship(
        "FinishedTask", backref="task", passive_deletes=True)
    comment = db.relationship('Comment', backref='task', passive_deletes=True)


class FinishedTask(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    finished_task = db.Column(db.String(20), nullable=False)
    operator_username = db.Column(db.String(20), nullable=False)
    finished_task_operator = db.Column(db.Integer, db.ForeignKey(
        "task.id", ondelete="CASCADE"))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=func.now(), nullable=False)
    operator = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"))
    task_id = db.Column(db.Integer, db.ForeignKey(
        'task.id', ondelete="CASCADE"))


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    task_author = db.Column(db.String(), nullable=False)
