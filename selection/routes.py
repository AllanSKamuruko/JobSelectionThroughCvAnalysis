from selection import app
from flask import render_template, redirect, url_for, flash, request
from selection.models import User, HR
from selection.forms import RegisterForm, LoginForm, HrForm
from selection import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/start')
def start_page():
    return render_template('start.html')

@app.route('/dash')
def dash_page():
    return render_template('dash.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('wtf_quiz'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/hrlogin', methods=['GET','POST'])
def hrlogin_page():
    form = HrForm()
    if form.validate_on_submit():
        attempted_emp = HR.query.filter_by(emp_number=form.emp_number.data).first()
        if attempted_emp and attempted_emp.check_password_correction1(
                attempted_password1=form.password1.data
        ):

            flash(f'Success! You are logged in as: {attempted_emp.emp_number}', category='success')
            return redirect(url_for('dash_page'))
        else:
            flash('Employee Number and password are not match! Please try again', category='danger')
            return redirect(url_for('home_page'))

    return render_template('hrlogin.html', form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for('home_page'))

