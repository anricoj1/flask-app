from flask import Flask, render_template, request, redirect, url_for, session, logging, flash, jsonify
from wtforms import Form, RadioField, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from functools import wraps
from passlib.hash import sha256_crypt
from src.user import *
from src.forms import SignUpForm
from src.admin import *
from src.follow import *
from query import *
import sq






app = Flask(__name__)


@app.route('/')
def index():
    query = 'SELECT * FROM User'
    value = fetchall(query)

    return render_template('base/home.html', value=value)



#to visit another users profile
@app.route('/profile/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def profile(user_id):
    return user_profile(user_id)




#view your profile (uses session)
@app.route('/account', methods=['GET', 'POST'])
@is_logged_in
def account():
    return display_prof()



# follow a user
@app.route('/follow_user/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def follow_user(user_id):
    if follow(user_id):
        c = sq.connection.cursor()
        c.execute('UPDATE Follower SET following = 1 WHERE user_name = %s AND user_id = %s', (session['email'], user_id))
        sq.connection.commit()
        return redirect(url_for('profile', user_id=user_id))
    else:
        return follow_user(user_id)



# unfollow a user
@app.route('/unfollow_user/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def unfollow_user(user_id):
    return unfollow(user_id)
















# User regisry section
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        return sign(form)
    else:
        return render_template('user/register.html', form=form)


# user login, user logs in from email
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return log()
    else:
        return render_template('user/login.html')


#logout route, clears session
@app.route('/logout')
@is_logged_in
def logout():
    return lout()


#admin only route role must be admin
@app.route('/admin_only')
@is_logged_in
def admin_only():
    if is_admin():
        mes = 'I am admin.'
        return render_template('base/home.html', mes=mes)
    else:
        return render_template('admin/Unauthorized.html')



#user dashboard (basic user info)
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    flash(session['first_name'] + ' Your Dashboard Lets You Manage Your Meets!', 'info')
    if is_admin():
        return admin_dashboard()
    else:
        return dash()

#edit your profile
@app.route('/edit_profile/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_profile(user_id):
    if is_admin():
        return modify_profile(user_id)
    elif is_current(user_id):
        return modify_profile(user_id)
    else:
        return render_template('admin/Unauthorized.html')


# delete profile
@app.route('/delete_profile/<string:user_id>', methods=['GET', 'POST'])
def ban_user(user_id):
    if is_admin():
        return ban(user_id)
    elif is_current(user_id):
        return redirect(url_for('secondchance'))
    else:
        return render_template('admin/Unauthorized.html')


# give user second chance before deleting account
@app.route('/secondchance', methods=['GET', 'POST'])
def secondchance():
    return render_template('admin/secondchance.html')







if __name__ == '__main__':
    app.secret_key='secret_key'
    app.run(debug=True)
