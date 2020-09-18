from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from social.model import User
from flask_login import current_user
from flask_wtf.html5 import EmailField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[EqualTo('confirm_password', message='Password Must Match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('SignUp')

    def validate_username(self, username):
        usrnam = User.query.filter_by(username=username.data).first()
        if usrnam:
            raise ValidationError('Username already taken select a new one')

    def validate_email(self, email):
        emal = User.query.filter_by(email=email.data).first()
        if emal:
            raise ValidationError('Already registered with this email')


class UpdateForm(FlaskForm):
    pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        emal = User.query.filter_by(email=email.data).first()
        if current_user.email != email.data:
            if emal:
                raise ValidationError('Already registered with this email')


class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit2 = SubmitField('Update Username')

    def validate_username(self, username):
        usr = User.query.filter_by(username=username.data).first()
        if usr:
            raise ValidationError('Username already taken select a new one')


class PasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[EqualTo('confirm_password', message='Password Must Match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit1 = SubmitField('Update Password')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')