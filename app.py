from flask import Flask, render_template, url_for, flash, redirect
from forms import CreateTripForm, LoginForm, RegistrationForm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a15205de7241c6ab3071b77da28c9623'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(50), nullable=False)

    teams = db.relationship('Team', backref='team_member', lazy=True)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}', '{self.image_file}')"


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(120), nullable=False)
    total_spendings = db.Column(db.Float, nullable=False)
    create_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    last_update_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    team_members = db.relationship('Team', backref='team_trip', lazy=True)
    expenses = db.relationship('Expense', backref='trip', lazy=True)

    def __repr__(self):
        return f"Trip('{self.route}', '{self.total_spendings}', '{self.create_date}', '{self.last_update_date}')"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    budget = db.Column(db.Float, nullable=False)
    credit = db.Column(db.Float, nullable=False)

    expenses = db.relationship(
        'Expense', backref='team_member_expense', lazy=True)

    def __repr__(self):
        return f"Team member('{self.trip}', '{self.user}', '{self.budget}', '{self.credit}')"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # foreign keys
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_member_id = db.Column(db.Integer, db.ForeignKey(
        'team_member.id'), nullable=False)
    # fields
    sum = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"Expense('{self.trip}', '{self.user}', '{self.sum}', '{self.category}', '{self.timestamp}', '{self.notes}')"


trips = [{
    'destination': 'Minsk - St. Petersburg',
    'date': '3/16/2019 - 3/18/2019',
    'total_spendings': 456.12
}, {
    'destination': 'Minsk - Gomel',
    'date': '12/11/2017 - 12/12/2017',
    'total_spendings': 52
}, {
    'destination': 'Minsk - Chicago',
    'date': '2/19/2016 - 3/18/2016',
    'total_spendings': 1873.23
}
]

users = [{
    'username': 'mary.gobra',
    'name': 'Mary Gobra',
    'email': 'mary.gobra@gmail.com',
    'balance': 512,
    'credit': 12,
    'profile_url': 'static/assets/palm1.png'
}, {
    'username': 'max.ersh',
    'name': 'Max',
    'email': 'max.ersh@gmail.com',
    'balance': 324,
    'credit': 42,
    'profile_url': 'static/assets/palm3.jpg'
}, {
    'username': 'iiiiigor',
    'name': 'Igor',
    'email': 'iiiigor@gmail.com',
    'balance': 542,
    'credit': 87,
    'profile_url': 'static/assets/palm3.jpg'
}
]

expenses = [{
    'category': 'Apartments',
    'sum': 134,
    'name': 'Mary',
    'timestamp': '1h ago'
}, {
    'category': 'Car',
    'sum': 335,
    'name': 'Igor',
    'timestamp': '2h ago'
}, {
    'category': 'Food',
    'sum': 87,
    'name': 'Mary',
    'timestamp': '9:50 am'
}
]


@app.route("/", methods=['GET', 'POST'])     # homepage
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = CreateTripForm()
    if form.validate_on_submit():
        return redirect(url_for('trip'))
    return render_template('home.html', posts=trips, title='Create new trip', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'mary.gobra' and form.password.data == '1953':
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check your credentials.')
    return render_template('login.html', title='Login', form=form)


@app.route("/trip")
def main():
    return render_template('trip.html', users=users, expenses=expenses)


if __name__ == '__main__':
    app.run(debug=True)
