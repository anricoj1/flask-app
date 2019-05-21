from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
from functools import wraps
import sq



#decides if a user is an admin or note based off session roles
def is_admin():
    current_role = session['role']
    print(current_role)
    if current_role:
        if current_role == 'admin':
            return True
        elif current_role == 'user':
            return False
    else:
        return 'User Unauthorized'



#admin dashboard, similar to user dashboard
def admin_dashboard():
    c = sq.connection.cursor()
    c.execute('SELECT * FROM User WHERE role="user"')
    users = c.fetchall()
    c.execute('SELECT * FROM Groups_table')
    groups = c.fetchall()
    c.execute('SELECT * FROM Events')
    events = c.fetchall()
    return render_template('admin/admin.html', message="I am admin", users=users, groups=groups, events=events)
