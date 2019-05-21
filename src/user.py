from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
from functools import wraps
from passlib.hash import sha256_crypt
from src.forms import EditProfile
import random
import sq


# session tracker
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized', 'danger')
            return redirect(url_for('login'))
    return wrap


#verify current user
def is_current(user_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT user_id FROM User WHERE user_id = %s', [user_id])
    user = c.fetchone()
    if result > 0:
        if session['user_ID'] == user.get('user_id'):
            return True
        else:
            return False
    else:
        'Unauthorized'



# validate email useage
def validate_email(form):
    emails = get_emails()

    if form.email.data in emails:
        print('Email In Use')
        return True
    else:
        print('Success')
        return False

    return 'Good Try'



#register function
def sign(form):
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        role = 'user'

        if validate_email(form):
            flash('Sorry, Email in use.', 'danger')
            return render_template('user/signup.html', form=form)

        else:

            c = sq.connection.cursor()

            c.execute('INSERT INTO User(first_name, last_name, email, password, role) VALUES(%s, %s, %s, %s, %s)', (fname, lname, email, password, role))

            sq.connection.commit()

            c.close()

            flash('you are now registered and can log in', 'info')

            return render_template('user/login.html', form=form)


# edit account info
def modify_profile(user_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT * FROM User WHERE user_id = %s', [user_id])

    user = c.fetchone()
    c.close()

    form = EditProfile(request.form)

    form.fname.data = user['first_name']
    form.lname.data = user['last_name']
    form.email.data = user['email']

    if request.method == 'POST' and form.validate():
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']


        c = sq.connection.cursor()

        c.execute('UPDATE User SET first_name=%s, last_name=%s, email=%s WHERE user_id=%s', (fname, lname, email, user_id))
        sq.connection.commit()

        c.close()

        flash('Account Updated', 'info')
        return redirect(url_for('index'))
    return render_template('user/edit_profile.html', form=form)



#login function
def log():
    email = request.form['email']
    password_cand = request.form['password']

    c = sq.connection.cursor()
    result = c.execute('SELECT * FROM User WHERE email = %s', [email])

    if result > 0:
        data = c.fetchone()
        password = data['password']

        if sha256_crypt.verify(password_cand, password):
            session['logged_in'] = True
            session['email'] = email
            session['user_ID'] = data['user_id']
            session['first_name'] = data['first_name']
            session['last_name'] = data['last_name']
            session['role'] = data['role']
            session['profile_pic'] = data['profile_pic_path']
            mess = get_flashed()
            flash(mess, 'info')

            return redirect(url_for('index')), data
        else:
            error = 'Invalid Login'
            return render_template('user/login.html', error=error)
    else:
        error = 'Email not found'
        return render_template('user/login.html')



#logout
def lout():
    session.clear()
    flash('You are now logged out', 'info')
    return redirect(url_for('login'))






# fetch all emails in db, append to list
def get_emails():
    c = sq.connection.cursor()
    result = c.execute('SELECT email FROM User')
    emails = c.fetchall()
    list = []
    for e in emails:
        email = e.get('email')
        list.append(email)

    return list

#dashboard
def dash():
    c = sq.connection.cursor()
    c.execute('SELECT group_id, name, creator, createdate FROM Groups_table WHERE creator = %s', [session['email']])
    group = c.fetchall()
    c.execute('SELECT e.event_id, a.event_id, name, user_name, description, attending FROM Events e INNER JOIN Attendee a ON a.event_id=e.event_id WHERE user_name = %s AND attending = 1', [session['email']])
    events = c.fetchall()

    c.execute('SELECT g.group_id, a.group_id, name, user_name, tag, creator, attending FROM Groups_table g INNER JOIN Attendee a ON a.group_id=g.group_id WHERE user_name = %s AND attending = 1', [session['email']])
    groups = c.fetchall()

    c.execute('SELECT * FROM Events WHERE creator = %s', [session['email']])
    created = c.fetchall()


    c.execute('SELECT COUNT(group_id) FROM Groups_table WHERE creator=%s UNION ALL SELECT COUNT(event_id) FROM Attendee WHERE user_name=%s AND attending=1 UNION ALL SELECT COUNT(group_id) FROM Attendee WHERE user_name=%s AND attending=1 UNION ALL SELECT COUNT(event_id) FROM Events WHERE creator=%s', [session['email'], session['email'], session['email'], session['email']])

    a = c.fetchone()
    e = c.fetchone()
    g = c.fetchone()
    t = c.fetchone()

    c1 = a.get('COUNT(group_id)')
    c2 = e.get('COUNT(group_id)')
    c3 = g.get('COUNT(group_id)')
    c4 = t.get('COUNT(group_id)')


    c.close()

    return render_template('user/dashboard.html', group=group, events=events, groups=groups, created=created, c1=c1, c2=c2, c3=c3, c4=c4)


# random messages at login
def get_flashed():
    strings = ['Welcome Back! ' + session['first_name'],
                'Greetings! ' + session['first_name'],
                'Look ' + session['first_name'] + ' Is Back!']


    ran_string = random.choice(strings)

    return ran_string




def user_profile(user_id):
    c = sq.connection.cursor()
    c.execute('SELECT * FROM User WHERE user_id = %s', [user_id])
    user = c.fetchone()

    c.execute('SELECT user_name, following FROM Follower WHERE user_id=%s AND following=1 AND user_name=%s', (user_id, session['email']))
    mem = c.fetchone()
    print(mem)

    return render_template('user/profile.html', user=user, mem=mem)



def display_prof():
    c = sq.connection.cursor()
    c.execute('SELECT g.group_id, a.group_id, name, user_name, tag, creator, attending FROM Groups_table g INNER JOIN Attendee a ON a.group_id=g.group_id WHERE user_name = %s AND attending = 1', [session['email']])
    groups = c.fetchall()

    return render_template('user/account.html', groups=groups)
