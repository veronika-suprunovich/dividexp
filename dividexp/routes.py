from flask import render_template, url_for, flash, redirect
from dividexp import app
from dividexp.forms import CreateTripForm, LoginForm, RegistrationForm, CreateTeamMemberForm, AddNewExpenseForm
from dividexp.models import User, Trip, Team, Expense


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
    'profile_url': 'static/assets/palm1.png'
}, {
    'username': 'iiiiigor',
    'name': 'Igor',
    'email': 'iiiigor@gmail.com',
    'balance': 542,
    'credit': 87,
    'profile_url': 'static/assets/palm1.png'
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


@app.route("/trip", methods=['GET', 'POST'])
def trip():
    expense_form = AddNewExpenseForm()
    team_member_form = CreateTeamMemberForm()

    if team_member_form.validate_on_submit():
        return redirect(url_for('trip'))
    elif expense_form.validate_on_submit():
        return redirect(url_for('trip'))

    return render_template('trip.html', users=users, expenses=expenses, tm_form=team_member_form, e_form=expense_form)
