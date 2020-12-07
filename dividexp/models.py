from dividexp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default.png')
    password = db.Column(db.String(50), nullable=False)

    teams = db.relationship('Team', backref='team_member', lazy=True)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}', '{self.image_file}')"


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(120), nullable=False)
    total_spendings = db.Column(db.Float, nullable=False, default=0.0)
    create_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    last_update_date = db.Column(
        db.DateTime, index=True, nullable=False, default=datetime.utcnow)

    team_members = db.relationship('Team', backref='team_trip', lazy=True)
    expenses = db.relationship('Expense', backref='trip', lazy=True)

    def __repr__(self):
        return f"Trip('{self.route}', '{self.total_spendings}', '{self.create_date}', '{self.last_update_date}')"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    budget = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    credit = db.Column(db.Float, nullable=False, default=0.0)

    expenses = db.relationship(
        'Expense', backref='team_member_expense', lazy=True)

    def __repr__(self):
        return f"Team('{self.trip_id}', '{self.user_id}', '{self.budget}', '{self.balance}', '{self.credit}')"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # foreign keys
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_member_id = db.Column(db.Integer, db.ForeignKey(
        'team.id'), nullable=False)
    # fields
    sum = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"Expense('{self.trip_id}', '{self.user_id}', '{self.team_member_id}', '{self.sum}', '{self.category}', '{self.notes}', '{self.timestamp}')"
