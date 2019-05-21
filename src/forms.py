from wtforms import Form, RadioField, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators

class SignUpForm(Form):
    fname = StringField('First', [validators.length(min=1, max=50)])
    lname = StringField('Last', [validators.length(min=1, max=50)])
    email = StringField('Email', )
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords dont match')
    ])
    confirm = PasswordField('Confirm Password')


class EditProfile(Form):
    fname = StringField('First', [validators.length(min=1, max=50)])
    lname = StringField('Last', [validators.length(min=1, max=50)])
    email = StringField('Email', )
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords dont match')
    ])
    confirm = PasswordField('Confirm Password')
