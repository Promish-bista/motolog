from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Trip, Maintenance, Expense
from datetime import datetime
from dotenv import load_dotenv
from controllers.auth_controller import AuthController
from controllers.trip_controller import TripController
from controllers.maintenance_controller import MaintenanceController
from controllers.expense_controller import ExpenseController
from utils.decorators import role_required
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ─── Auth Routes ───────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user, error = AuthController.register_user(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password'],
            bike_model=request.form.get('bike_model', ''),
            admin_code=request.form.get('admin_code', '')
        )
        if error:
            flash(error, 'danger')
            return redirect(url_for('register'))
        flash(f'Account created as {user.role}! Log in now.', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', mode='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = AuthController.login_user_check(
            email=request.form['email'],
            password=request.form['password']
        )
        if user:
            login_user(user)
            if user.is_admin():
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', mode='login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ─── Rider Dashboard ───────────────────────
@app.route('/')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    trips       = TripController.get_user_trips(current_user.id)[:5]
    maintenance = MaintenanceController.get_user_logs(current_user.id)[:5]
    expenses    = ExpenseController.get_user_expenses(current_user.id)[:5]
    total_spend = ExpenseController.get_total_spend(current_user.id)
    return render_template('index.html', trips=trips, maintenance=maintenance,
                           expenses=expenses, total_spend=total_spend)

# ─── Admin Routes ──────────────────────────
@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    users       = AuthController.get_all_users()
    trips       = TripController.get_all_trips()
    maintenance = MaintenanceController.get_all_logs()
    expenses    = ExpenseController.get_all_expenses()
    total_spend = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    return render_template('admin_dashboard.html', users=users, trips=trips,
                           maintenance=maintenance, expenses=expenses,
                           total_spend=total_spend)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin_dashboard'))
    AuthController.delete_user(user_id)
    flash('User deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_trip/<int:trip_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_trip(trip_id):
    TripController.delete_trip(trip_id)
    flash('Trip deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_expense(expense_id):
    ExpenseController.delete_expense(expense_id)
    flash('Expense deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

# ─── Trip Routes ───────────────────────────
@app.route('/trips')
@login_required
def trips():
    all_trips = TripController.get_user_trips(current_user.id)
    return render_template('trips.html', trips=all_trips)

@app.route('/trips/new', methods=['GET', 'POST'])
@login_required
def new_trip():
    if request.method == 'POST':
        TripController.create_trip(current_user.id, request.form)
        flash('Trip logged!', 'success')
        return redirect(url_for('trips'))
    return render_template('trip_detail.html', trip=None, mode='new')

@app.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    trip = TripController.get_trip_by_id(trip_id)
    if trip.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('trips'))
    if request.method == 'POST':
        TripController.update_trip(trip_id, request.form)
        flash('Trip updated.', 'success')
        return redirect(url_for('trips'))
    return render_template('trip_detail.html', trip=trip, mode='edit')

@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = TripController.get_trip_by_id(trip_id)
    if trip.user_id == current_user.id:
        TripController.delete_trip(trip_id)
        flash('Trip deleted.', 'info')
    return redirect(url_for('trips'))

# ─── Maintenance Routes ────────────────────
@app.route('/maintenance')
@login_required
def maintenance():
    logs = MaintenanceController.get_user_logs(current_user.id)
    return render_template('maintenance.html', logs=logs)

@app.route('/maintenance/new', methods=['POST'])
@login_required
def new_maintenance():
    MaintenanceController.create_log(current_user.id, request.form)
    flash('Service log saved.', 'success')
    return redirect(url_for('maintenance'))

@app.route('/maintenance/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_maintenance(log_id):
    log = MaintenanceController.get_user_logs(current_user.id)
    MaintenanceController.delete_log(log_id)
    return redirect(url_for('maintenance'))

# ─── Expense Routes ────────────────────────
@app.route('/expenses')
@login_required
def expenses():
    all_expenses = ExpenseController.get_user_expenses(current_user.id)
    trips        = TripController.get_user_trips(current_user.id)
    return render_template('expenses.html', expenses=all_expenses, trips=trips)

@app.route('/expenses/new', methods=['POST'])
@login_required
def new_expense():
    ExpenseController.create_expense(current_user.id, request.form)
    flash('Expense recorded.', 'success')
    return redirect(url_for('expenses'))

@app.route('/expenses/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    ExpenseController.delete_expense(expense_id)
    return redirect(url_for('expenses'))

if __name__ == '__main__':
    app.run(debug=True)