from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, IntegerField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField("ID лидера", validators=[DataRequired()])
    job = TextAreaField(validators=[DataRequired()])
    work_size = IntegerField("Размер работы")
    collaborators = StringField("Соавторы")
    start_date = DateTimeField("Начало работы")
    end_date = DateTimeField("Конец работы")
    is_finished = BooleanField("Работа закончена?")

    submit = SubmitField("Отправить")
