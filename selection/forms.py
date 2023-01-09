from tkinter.tix import Form

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from selection.models import User, HR, CorrectAnswer


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')



    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class HrForm(FlaskForm):
    emp_number = IntegerField(label='Employee Number', validators=[DataRequired()])
    password1 = StringField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

'''class PopQuiz(FlaskForm):
    class Meta:
        csrf = False
    q1 = RadioField(
        "The answer to question one is False.",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[CorrectAnswer('False')]
        )
'''
