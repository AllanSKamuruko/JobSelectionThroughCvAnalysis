from wtforms import ValidationError

from selection import db, login_manager
from selection import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    candidate = db.relationship('Question', backref='owned_user', lazy=True)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Question(db.Model):
    q_id = db.Column(db.Integer(), primary_key=True)
    result = db.Column(db.Integer(), nullable= False)
    candidate = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def result(self, user):
        self.candidate = user.id
        user.result += self.price
        db.session.commit()


class HR(db.Model, UserMixin):
    emp_number = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    password_hr = db.Column(db.String(), nullable=False)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hr = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction1(self, attempted_password1):
        return bcrypt.check_password_hash(self.password_hr, attempted_password1)

    def get_emp_number(self):
        return (self.emp_number)

class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        message = 'Incorrect answer.'

        if field.data != self.answer:
            raise ValidationError(message)

