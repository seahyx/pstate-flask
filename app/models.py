from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# name of the group
	name = db.Column(db.String(32), index=True, unique=True)

	# link to users
	users = db.relationship('User', backref='group', lazy='dynamic')

	def __repr__(self):
		return '<{} Group {}>'.format(self.id, self.name)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# link to group
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

	# rank
	rank = db.Column(db.String(10), index=True)

	# full name
	name = db.Column(db.String(32), index=True, unique=True)

	# account password
	password_hash = db.Column(db.String(128))

	# email
	email = db.Column(db.String(120), index=True, unique=True)

	# mobile phone number
	hp = db.Column(db.String(8), index=True, unique=True)

	# account permission level
	account_type = db.Column(db.Integer, index=True)

	# link to parade state
	parade_states = db.relationship('PState', backref='user', lazy='dynamic')

	ACCOUNT_TYPES = [(0, 'Root'), (1, 'Admin'), (2, 'User')]

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_account_type_name(self):
		return self.ACCOUNT_TYPES[self.account_type][1]
	
	def has_admin_rights(self):
		return (self.account_type == 0 or self.account_type == 1)

	def __repr__(self):
		return '<{} {} {},\ngroup_id/group: {} {},\naccount type: {}>'.format(self.id, self.rank, self.name, self.group_id, self.group.name, self.get_account_type_name())

# Parade state table linked to every user.
class PState(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	# link to user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	# date of parade state
	date = db.Column(db.Date, index=True)

	# parade state is till xxx. Otherwise it will be the same as date.
	end_date = db.Column(db.Date, index=True)

	# primary parade state
	state_am = db.Column(db.String(32), index=True)
	state_am_reason = db.Column(db.String(32), index=True)
	state_am_location = db.Column(db.String(32), index=True)

	# boolean for if there is two different states
	full_day = db.Column(db.Boolean, index=True)
	
	# secondary parade state, left empty (null) if pstate is whole day
	state_pm = db.Column(db.String(32), index=True)
	state_pm_reason = db.Column(db.String(32), index=True)
	state_pm_location = db.Column(db.String(32), index=True)

	def format_date(self, date):
		return date.strftime('%d%m%y')

	def get_parade_state(self):

		if self.state_am is None:
			return 'Error: Valid parade state is not provided'
		
		state = self.state_am

		if self.state_am_location is not None:
			state += '@{}'.format(self.state_am_location)
		
		if self.state_am_reason is not None:
			state += ' ({})'.format(self.state_am_reason)

		if self.full_day is not None and not self.full_day:
			# has both am and pm pstate
			state += '/{}'.format(self.state_pm)

			if self.state_pm_location is not None:
				state += '@{}'.format(self.state_pm_location)
			
			if self.state_pm_reason is not None:
				state += ' ({})'.format(self.state_pm_reason)
		
		if self.end_date is not None:
			# has an end date
			state += ' till {}'.format(self.format_date(self.end_date))
		
		return state
	
	def __repr__(self):
		return '<{} PState {}\nformatted pstate: {},\nfull_day: {},\nstate_am: {}, state_am_reason: {}, state_am_location: {},\nstate_pm: {}, state_pm_reason: {}, state_pm_location: {}>'.format(self.id, self.format_date(self.date), self.get_parade_state(), self.full_day, self.state_am, self.state_am_reason, self.state_am_location, self.state_pm, self.state_pm_reason, self.state_pm_location)