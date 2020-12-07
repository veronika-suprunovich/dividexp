from numpy import zeros
from dividexp import db
from dividexp.models import User, Team, Trip, Expense
from math import fabs


class TripManager:
    def __init__(self):
        self.id = 0
        self.keys = {}
        self.size = 1
        self.expenses = []
        self.team = []

    def set_id(self, trip_id):
        self.id = trip_id

    def enumerate_members(self, team):
        for member in team:
            print(member.user_id)
            if member.user_id in self.keys:
                continue
            self.keys[member.user_id] = len(self.keys)

        print(self.keys)

    def edit_expense_table(self, row, sum):
        credit = sum / self.size

        for column in range(0, self.size):
            if(row == column):
                self.expense_table[row,
                                   column] = self.expense_table[row, column] + sum
                continue
            if (self.expense_table[column, row] != 0):
                new_credit = self.expense_table[column, row] - credit
                if new_credit > 0:
                    self.expense_table[column, row] = new_credit
                else:
                    self.expense_table[row, column] = fabs(new_credit)
                    self.expense_table[column, row] = 0
            else:
                self.expense_table[row,
                                   column] = self.expense_table[row, column] + credit

    def fill_table(self, team, expenses):
        self.size = len(team)
        self.expense_table = zeros((self.size, self.size))
        self.enumerate_members(team)

        for e in expenses:
            # get row num
            row = self.keys.get(e.user_id)
            self.edit_expense_table(row, e.sum)

    def recount_user_budget(self, user_id, col):
        # team member id
        user = Team.query.get(user_id)
        credit = 0.0
        for row in range(0, self.size):
            if(row == col):
                user.balance = user.budget - self.expense_table[col, col]
            else:
                credit = credit + self.expense_table[row, col]

        user.credit = credit
        db.session.commit()

    def recount_all_users_budget(self):

        for user in self.keys:
            self.recount_user_budget(user, self.keys.get(user))

        self.collect_users()

    def collect_users(self):
        self.team.clear()
        # get team members of the trip
        trip = Trip.query.get(self.id)
        team_members = trip.team_members
        for each_member in team_members:
            user = User.query.filter_by(id=each_member.user_id).first()
            self.recount_user_budget(each_member.id, self.keys.get(user.id))
            self.team.append({
                'id': each_member.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'image_file': user.image_file,
                'budget': round(each_member.balance, 2),
                'credit': round(each_member.credit, 2),
                'progress_bar_value': int(100.0 * each_member.balance / each_member.budget)
            })

    def collect_expenses(self):
        self.expenses.clear()
        all_expenses = Trip.query.filter_by(id=self.id).first().expenses

        for each_expense in all_expenses:
            user = User.query.get(each_expense.user_id)

            self.expenses.append({
                'category': each_expense.category,
                'sum': each_expense.sum,
                'name': user.name,
                'timestamp': each_expense.timestamp.strftime('%I:%M %p'),
            })

    def add_expense(self, username, category, sum, notes):
        # commit changes to the database
        user = User.query.filter_by(username=username).first()
        team_member = User.query.join(User.teams).filter(
            User.username == username, Team.trip_id == self.id).first()
        expense = Expense(trip_id=self.id, user_id=user.id, team_member_id=team_member.id,
                          sum=sum, category=category, notes=notes)
        db.session.add(expense)
        trip = Trip.query.get(self.id)
        trip.total_spendings = trip.total_spendings + expense.sum
        db.session.commit()
        new_expense = {
            'category': expense.category,
            'sum': expense.sum,
            'name': user.name,
            'timestamp': expense.timestamp.strftime('%I:%M %p'),
        }
        self.expenses.append(new_expense)

        self.edit_expense_table(self.keys.get(user.id), sum)
        self.recount_all_users_budget()

    def add_team_member(self, username, budget):

        user = User.query.filter_by(username=username).first()
        if user:
            # user is in a database
            team_member = Team(trip_id=self.id, user_id=user.id,
                               budget=budget, balance=budget)
            db.session.add(team_member)
            db.session.commit()

            new_user = {
                'id': team_member.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'image_file': user.image_file,
                'budget': round(team_member.balance),
                'credit': round(team_member.credit),
                'progress_bar_value': int(100.0 * team_member.balance / team_member.budget)
            }
            self.team.append(new_user)
            return True
        else:
            return False
