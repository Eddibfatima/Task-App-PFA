from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .models import User, Task,  FinishedTask, Comment, Search
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route('/register')
def register():
    return render_template("register.html")


@views.route('/login')
def login():
    return render_template('login.html')


@views.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.all()
    user = User.query.all()
    finished = FinishedTask.query.all()
    return render_template("dashboard.html", user=user, tasks=tasks, connected_user=current_user, finished=finished)


@views.route("/profile/<id>", methods=["POST", "GET"])
@login_required
def profile(id):
    profile = User.query.get_or_404(id)
    if request.method == "POST" and current_user:
        profile.username = request.form.get('username')
        profile.first_name = request.form.get('first_name')
        profile.last_name = request.form.get('last_name')
        profile.id = profile.id
        profile.job = request.form.get('job')
        profile.email = request.form.get('email')
        profile.password = generate_password_hash(
            request.form.get('password'), method="sha256")
        picture = request.files['picture']
        filename = secure_filename(picture.filename)
        mimetype = picture.mimetype
        profile.picture = picture.read()
        profile.mimetype = mimetype
        profile.filename = filename
        db.session.commit()
        return redirect(url_for('views.profile', user=current_user, id=current_user.id))
    return render_template("profile.html", user=current_user, id=current_user.id,)


@views.route("/projects", methods=["GET", "POST"])
@login_required
def project():
    return render_template("projects.html", user=current_user)


@views.route('/tasks', methods=["POST", "GET"])
@login_required
def tasks():
    task = Task.query

    if current_user and request.method == "POST":
        task.open_task = request.form.get("task")
        task.task_descriptif = request.form.get("task_descriptif")
        tasks = Task(open_task=task.open_task, ongoing_task=task.open_task,
                     operator=current_user.id, task_descriptif=task.task_descriptif)
        db.session.add(tasks)
        db.session.commit()
    return render_template("tasks.html", user=current_user, tasks=task)


@views.route('/finished/<id>', methods=['POST', "GET"])
@login_required
def finished(id):
    task = Task.query.filter_by(id=id).first()
    finished = FinishedTask.query.filter_by(id=id).first()
    finishedt = FinishedTask(finished_task=task.open_task,
                             finished_task_operator=task.operator, operator_username=task.user.username)
    db.session.add(finishedt)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.dashboard", task=task, finishedt=finished, user=current_user))


@views.route('/update/<id>', methods=["POST", "GET"])
@ login_required
def update(id):
    task = Task.query.get(id)
    if current_user and request.method == "POST":
        task.open_task = request.form["task_to_update"]
        task.ongoing_task = request.form['task_to_update']
        task.task_descriptif = request.form['task_descriptif_to_update']
        db.session.commit()
    return render_template("update.html", task=task)


@views.route('/delete/<id>', methods=["POST", "GET"])
@ login_required
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('views.dashboard', task=task))


@views.route('/delete_descriptif/<task_descriptif>', methods=["POST", "GET"])
@login_required
def delete_descriptif(task_descriptif):
    task = Task.query.filter_by(task_descriptif=task_descriptif).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully.")
    else:
        flash("Task not found.")

    return redirect(url_for('views.dashboard'))


@views.route("/projects/<username>")
@login_required
def projects(username):
    user = User.query.filter_by(username=username).first()
    task = user.task
    finishedtasks = FinishedTask.query.filter_by(
        finished_task_operator=current_user.id).all()
    return render_template("projects.html", user=current_user, task=task, finishedtasks=finishedtasks, username=username)


@views.route("/description/<task_id>", methods=["POST", "GET"])
@login_required
def description(task_id):
    tasks = Task.query.all()
    task = Task.query.filter_by(id=task_id).first()
    text_comment = request.form.get('comment')
    if text_comment is not None:
        comment = Comment(comment=text_comment,
                          operator=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()
    comments = Comment.query.all()
    return render_template("description.html", user=current_user, tasks=tasks, task=task,  comments=comments)


@views.route("/update_comment/<comment_id>", methods=["GET", "POST"])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        flash("comment does not exist")

    if comment.operator != current_user.id:
        flash("yout not allowed to modify this Comment")
    if request.method == "POST":
        new_comment = request.form.get("comment")
        comment.comment = new_comment
        db.session.commit()
        flash("Comment updated successfully.")
        return redirect(url_for("views.description", task_id=comment.task_id))

    return render_template("update_comment.html", comment=comment)


@views.route("/delete_comment/<comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment.operator != current_user.id:
        flash("Comment was not deleted")

    if request.method == "POST":
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully.")
        return redirect(url_for("views.description", task_id=comment.task_id))

    return render_template("delete_comment.html", comment=comment)


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


@views.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@views.route("/search_result", methods=["POST"])
@login_required
def search_result():
    form = SearchForm()
    search = Search.query
    output_searched = form.searched.data
    search_result = search.filter(Search.task.like("%"+output_searched+"%"))
    search_result = search_result.order_by(Search.task).all()
    return render_template("search_result.html", user=current_user, output=output_searched, form=form, search_result=search_result)
