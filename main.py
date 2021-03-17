import datetime

from flask import Flask, render_template, redirect, request, make_response, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.jobs import JobsForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def add_users(db_sess):
    user1 = User(surname="Scott",
                 name="Ridley",
                 age=21,
                 position="captain",
                 speciality="research engineer",
                 address="module_1",
                 email="scott_chief@mars.org",
                 hashed_password="cap")
    user2 = User(surname="Andy",
                 name="Weir",
                 age=19,
                 position="colonist",
                 speciality="pilot",
                 address="module_2",
                 email="andy_col@mars.org",
                 hashed_password="pil")
    user3 = User(surname="Mark",
                 name="Watney",
                 age=21,
                 position="colonist",
                 speciality="doctor",
                 address="module_3",
                 email="doc_mark@mars.org",
                 hashed_password="doc")
    user1.set_password(user1.hashed_password)
    user2.set_password(user2.hashed_password)
    user3.set_password(user3.hashed_password)
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.commit()


def add_jobs(db_sess):
    job1 = Jobs(team_leader=1,
                job="deployment of residential modules 1 and 2",
                work_size=15,
                collaborators="2, 3",
                is_finished=False)
    job2 = Jobs(team_leader=2,
                job="exploration of mineral resources",
                work_size=12,
                collaborators="4, 3",
                is_finished=False)
    job3 = Jobs(team_leader=3,
                job="development of a management system",
                work_size=25,
                collaborators="5",
                is_finished=False)

    db_sess.add(job1)
    db_sess.add(job2)
    db_sess.add(job3)
    db_sess.commit()


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
    db_sess = db_session.create_session()

    add_users(db_sess)
    add_jobs(db_sess)

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
