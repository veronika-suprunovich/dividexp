from flask import render_template, url_for, flash, redirect, request
from dividexp import app, db, bcrypt
from dividexp.forms import CreateTripForm, LoginForm, RegistrationForm, CreateTeamMemberForm, AddNewExpenseForm
from dividexp.models import User, Trip, Team, Expense
from flask_login import login_user, logout_user, current_user, login_required


# users = [{
#     'username': 'mary.gobra',
#     'name': 'Mary Gobra',
#     'email': 'mary.gobra@gmail.com',
#     'balance': 512,
#     'credit': 12,
#     'profile_url': 'static/assets/palm3.jpg'
# }, {
#     'username': 'max.ersh',
#     'name': 'Max',
#     'email': 'max.ersh@gmail.com',
#     'balance': 324,
#     'credit': 42,
#     'profile_url': 'static/assets/palm3.jpg'
# }, {
#     'username': 'iiiiigor',
#     'name': 'Igor',
#     'email': 'iiiigor@gmail.com',
#     'balance': 542,
#     'credit': 87,
#     'profile_url': 'static/assets/palm3.jpg'
# }
# ]
#
# expenses = [{
#     'category': 'Apartments',
#     'sum': 134,
#     'name': 'Mary',
#     'timestamp': '1h ago'
# }, {
#     'category': 'Car',
#     'sum': 335,
#     'name': 'Igor',
#     'timestamp': '2h ago'
# }, {
#     'category': 'Food',
#     'sum': 87,
#     'name': 'Mary',
#     'timestamp': '9:50 am'
# }]


def collect_trips(id):
    trips = []
    # get list of user's teams
    teams = Team.query.filter_by(user_id=id).all()

    for each_team in teams:
        # get trip of each team
        trip = Trip.query.filter_by(id=each_team.trip_id).first()
        trips.append({
            'id': trip.id,
            'route': trip.route,
            'create_date': trip.create_date.strftime('%d/%m/%Y'),
            'last_update_date': trip.last_update_date.strftime('%d/%m/%Y'),
            'total_spendings': trip.total_spendings
        })

    return reversed(trips)


def collect_users(trip_id):
    users = []

    # get team members of the trip
    trip = Trip.query.get(trip_id)
    team_members = trip.team_members

    for each_member in team_members:
        user = User.query.filter_by(id=each_member.user_id).first()
        users.append({
            'id': each_member.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'image_file': user.image_file,
            'budget': each_member.budget,
            'credit': each_member.credit
        })

    return reversed(users)


@app.route("/", methods=['GET', 'POST'])     # homepage
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        trips = collect_trips(current_user.id)
    form = CreateTripForm()
    if form.validate_on_submit():
        new_trip = Trip(route=form.source.data + ' - ' + form.destination.data)
        db.session.add(new_trip)
        db.session.commit()
        team_member = Team(trip_id=new_trip.id, user_id=current_user.id, budget=form.budget.data, credit=0.00)
        db.session.add(team_member)
        db.session.commit()
        return redirect(url_for('trip'))
    return render_template('home.html', trips=trips, title='Create new trip', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check your credentials.')
    return render_template('login.html', title='Login', form=form)


@app.route("/trip/<int:trip_id>", methods=['GET', 'POST'])
@login_required
def trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    expense_form = AddNewExpenseForm()
    team_member_form = CreateTeamMemberForm()

    users = collect_users(trip_id=trip.id)
    expenses = trip.expenses

    if team_member_form.validate_on_submit():
        return redirect(url_for('trip', trip_id=trip.id))
    elif expense_form.validate_on_submit():
        return redirect(url_for('trip', trip_id=trip.id))

    return render_template('trip.html', title=trip.route, users=users, expenses=expenses, tm_form=team_member_form, e_form=expense_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
