from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
#this allows us to update a jpg or png file to have their profile pic updated
#1-5 is related to forms 8-9 is related to users
from flask_login import current_user
from puppycompanyblog.models import User




class LoginForm(FlaskForm):
    email = StringField('Email',render_kw={'placeholder':'Please Enter Your Email'}, validators=[DataRequired(), Email()])
    password = PasswordField('Password',render_kw={'placeholder':'Password'}, validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', render_kw={'placeholder':'Please Enter Your Email'}, validators=[DataRequired(),Email()])
    username = StringField('Username',render_kw={'placeholder':'Username'}, validators=[DataRequired()])
    password = PasswordField('Password',render_kw={'placeholder':'Password'}, validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password',render_kw={'placeholder':'Confirm Password'}, validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            #if User model, imported from above, gets queried to see if exist
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
