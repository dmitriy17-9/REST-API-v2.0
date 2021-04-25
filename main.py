import datetime
import os

from waitress import serve
from flask import Flask, render_template, redirect, request, make_response, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session, users_resource, jobs_resource
from data.jobs import Jobs
from data.users import User
from forms.jobs import JobsForm
from forms.user import LoginForm, RegisterForm
from data.add_data_db import add_user, add_jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)
# для списка объектов
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
# для одного объекта
api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')

# для списка объектов
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
# для одного объекта
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", title="Миссия")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/login_job', methods=['GET', 'POST'])
def login_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_name = "db/mars_one.db"
    db_session.global_init(db_name)

    # add_user()
    # add_jobs()

    port = int(os.environ.get('PORT', 8080))
    # app.run(port=port, host="0.0.0.0")

    # с дефаултными значениями будет не более 4 потов
    serve(app, port=port, host="0.0.0.0")


if __name__ == '__main__':
    main()
