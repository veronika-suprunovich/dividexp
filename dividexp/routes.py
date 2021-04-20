from flask import render_template, url_for, flash, redirect, request
from dividexp import app, db, bcrypt, manage
from dividexp.forms import CreateTripForm, LoginForm, RegistrationForm, CreateTeamMemberForm, AddNewExpenseForm
from dividexp.models import Users, Trips, Teams
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/", methods=['GET', 'POST'])     # homepage
@app.route("/home", methods=['GET', 'POST'])
def home():
    trips = []
    if current_user.is_authenticated:
        trips = manage.collect_trips(current_user.id)
    form = CreateTripForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_trip = Trips(route=form.source.data +
                            ' - ' + form.destination.data)
            db.session.add(new_trip)
            db.session.commit()
            print(form.budget.data)
            team_member = Teams(trip_id=new_trip.id, user_id=current_user.id,
                               budget=form.budget.data, balance=form.budget.data)
            db.session.add(team_member)
            db.session.commit()
            return redirect(url_for('trip', trip_id=new_trip.id))
        else:
            return redirect(url_for('login'))
    return render_template('home.html', trips=reversed(trips), title='Create new trip', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = Users(name=form.name.data, username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
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

    trip = Trips.query.get_or_404(trip_id)

    if (manage.id != trip.id):
        manage.clear()
        manage.set_id(trip_id)
        manage.fill_table(trip.team_members, trip.expenses)
        manage.collect_expenses()
        manage.collect_users()

    expense_form = AddNewExpenseForm(split=True)
    team_member_form = CreateTeamMemberForm()

    if team_member_form.validate_on_submit():
        # check whether the user is already in the team
        existing = Users.query.join(Users.teams).filter(
            Users.username == team_member_form.username.data, Teams.trip_id == trip.id).first()
        if(existing is None):
            if manage.add_team_member(team_member_form.username.data, team_member_form.budget.data) is False:
                flash("""Couldn't find DivideXp account""")
            else:
                manage.fill_table(trip.team_members, trip.expenses)
                manage.collect_users()
        else:
            flash('The user is already in your team')
        return redirect(url_for('trip', trip_id=trip.id))
    elif expense_form.validate_on_submit():
        if expense_form.split.data is True:
            manage.add_joint_expense(expense_form.username.data, expense_form.category.data, expense_form.sum.data, expense_form.notes.data)
        else:
            manage.add_expense(expense_form.username.data, expense_form.category.data, expense_form.sum.data, expense_form.notes.data)
        return redirect(url_for('trip', trip_id=trip.id))

    labels, values = manage.get_chart_items()

    return render_template('trip.html', title=trip.route, users=reversed(manage.team), expenses=reversed(manage.expenses), tm_form=team_member_form, e_form=expense_form, values=values, labels=labels)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
