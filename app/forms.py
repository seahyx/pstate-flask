from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Email
from app.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired('Email is required, please'), Email('Please provide a valid email, please')])
	password = PasswordField('Password', validators=[DataRequired('Password is required, please')])
	rmb_me = BooleanField('Remember Me')
	submit = SubmitField('Enter')

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired('Email required lah'), Email('Provide a valid email address, please')])

	password = PasswordField('Password', validators=[DataRequired('Password also required lah'), Length(min=4, message='Password must be at least %(min)d characters long eh')])

	password2 = PasswordField('Confirm Password', validators=[DataRequired('Confirm the password leh'), EqualTo('password', 'Password type second time must be same eh')])

	account_type = SelectField('Account Permissions', choices=User.ACCOUNT_TYPES[1:len(User.ACCOUNT_TYPES)], coerce=int, default=2)

	submit = SubmitField('Register')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('This email address chosen already lah, choose another one')

class ChangePasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired('Password also required lah'), Length(min=4, message='Password must be at least %(min)d characters long eh')])

	password2 = PasswordField('Confirm Password', validators=[DataRequired('Confirm the password leh'), EqualTo('password', 'Password type second time must be same eh')])

	submit = SubmitField('Register')