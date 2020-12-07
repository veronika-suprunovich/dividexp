from flask import render_template, url_for, flash, redirect, request
from dividexp import app, db, bcrypt
from dividexp.forms import CreateTripForm, LoginForm, RegistrationForm, CreateTeamMemberForm, AddNewExpenseForm
from dividexp.models import User, Trip, Team
from flask_login import login_user, logout_user, current_user, login_required
from dividexp.manager import TripManager

expense_table = TripManager()


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


@app.route("/", methods=['GET', 'POST'])     # homepage
@app.route("/home", methods=['GET', 'POST'])
def home():
    trips = []
    if current_user.is_authenticated:
        trips = collect_trips(current_user.id)
    form = CreateTripForm()
    if form.validate_on_submit():
        new_trip = Trip(route=form.source.data + ' - ' + form.destination.data)
        db.session.add(new_trip)
        db.session.commit()
        print(form.budget.data)
        team_member = Team(trip_id=new_trip.id, user_id=current_user.id,
                           budget=form.budget.data, balance=form.budget.data)
        db.session.add(team_member)
        db.session.commit()
        return redirect(url_for('trip', trip_id=new_trip.id))
    return render_template('home.html', trips=trips, title='Create new trip', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data,
                    email=form.email.data, password=hashed_password)
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

    if (expense_table.id != trip.id):
        expense_table.set_id(trip_id)
        expense_table.fill_table(trip.team_members, trip.expenses)
        expense_table.collect_users()
        expense_table.collect_expenses()

    expense_form = AddNewExpenseForm()
    team_member_form = CreateTeamMemberForm()

    if team_member_form.validate_on_submit():
        # check whether the user is already in the team
        existing = User.query.join(User.teams).filter(
            User.username == team_member_form.username.data, Team.trip_id == trip.id).first()
        if(existing is None):
            if expense_table.add_team_member(team_member_form.username.data, team_member_form.budget.data) is False:
                flash("""Couldn't find DivideXp account""")
        else:
            flash('The user is already in your team')
    elif expense_form.validate_on_submit():
        expense_table.add_expense(
            expense_form.username.data, expense_form.category.data, expense_form.sum.data, expense_form.notes.data)

    return render_template('trip.html', title=trip.route, users=reversed(expense_table.team), expenses=reversed(expense_table.expenses), tm_form=team_member_form, e_form=expense_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
