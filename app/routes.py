from flask import render_template, jsonify, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.models import User
from app.permissions import PermissionsManager
from werkzeug.urls import url_parse
import time
# import socket

# Function to get ip address of host
# def get_ip_address():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]

# host_ip = get_ip_address()

permissions = PermissionsManager()
permissions.redirect_view = 'index'


@app.route('/')
@app.route('/home/')
@login_required
def index():
	return render_template('home.html', title='Home')


@app.route('/login/', methods=['GET', 'POST'])
def login():
	
	# If user is logged in and navigates to this page somehow
	if current_user.is_authenticated:
		# Redirect back to home page
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():

		# Find a user by email from the User db table
		user = User.query.filter_by(email=form.email.data).first()

		# Wrong email or password
		if not user or not user.check_password(form.password.data):
			fail_count = int(request.args.get('fail_count', 0))
			if fail_count != 99:
				fail_count += 1
			print(fail_count)
			return redirect(url_for('login', prev_email=form.email.data, fail_count=fail_count))

		# Correct email and password
		login_user(user, remember=form.rmb_me.data)

		next_page = request.args.get('next')
		# Netloc tests if next is pointed towards other site, which can link to malicious sites. Thus not accepting the redirect if it has value.
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')

		return redirect(next_page)
	
	fail_count = int(request.args.get('fail_count', 0))
	prev_email = request.args.get('prev_email')
	
	return render_template('login.html', title='Login', form=form, no_header=True, email=prev_email, fail_count=fail_count)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration/', methods=['GET', 'POST'])
@login_required
@permissions.admin_required
def registration():

	form = RegistrationForm()

	if form.validate_on_submit():
		user = User(email=form.email.data, account_type=form.account_type.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('{} {} has been created'.format(user.get_account_type_name(), user.email))

		next_page = request.args.get('next')
		# Netloc tests if next is pointed towards other site, which can link to malicious sites. Thus not accepting the redirect if it has value.
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')

		return redirect(next_page)

	return render_template('registration.html', title='Create new account', form=form)


@app.route('/dashboard/')
@login_required
@permissions.admin_required
def dashboard():
	if request.args.get('rmId') and request.args.get('rmId').isdigit():
		removal_id = int(request.args.get('rmId'))
		print('Dashboard: Account of list id {} requested'.format(removal_id))
		
		# Now check if the number is valid and that the user is safe to delete
		user = User.query.filter_by(id=removal_id).first()
		if (user):
			# The user exists
			if ((user.id != current_user.id) and user.account_type != 0):
				# The user is not the currently logged in user or root, thus can be safely deleted
				db.session.delete(user)
				db.session.commit()
				print('Success: User with email {}, id of {} is deleted'.format(user.email, removal_id))
				flash('Success: User with email {}, id of {} is deleted'.format(user.email, removal_id))
			else:
				# The user is root or current user, thus cannot be removed
				print('Error: User with email {}, id of {} cannot be deleted'.format(user.email, removal_id))
				flash('Error: User with email {}, id of {} cannot be deleted'.format(user.email, removal_id))
		else:
			# The user doesn't exist
			print('Error: User with id of {} does not exist'.format(removal_id))
			flash('Error: User with id of {} does not exist'.format(removal_id))

	return render_template('dashboard.html', title='Admin Dashboard', users=User.query.order_by(User.account_type).order_by(User.email).all())


@app.route('/dashboard/change-pass/<email>/', methods=['GET', 'POST'])
@login_required
@permissions.admin_required
def change_pass(email):
	user = User.query.filter_by(email=email).first_or_404()

	form = ChangePasswordForm()

	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Success: Password for {} {} has been changed'.format(user.get_account_type_name(), user.email))
		return(redirect(url_for('dashboard')))
	
	return(render_template('change-pass.html', title='Change password', form=form, user=user))

	return

