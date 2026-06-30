from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Trip, Maintenance, Expense
from datetime import datetime
from dotenv import load_dotenv
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username   = request.form['username']
        email      = request.form['email']
        password   = request.form['password']
        bike_model = request.form.get('bike_model', '')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed_pw, bike_model=bike_model)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Log in now.', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', mode='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user     = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', mode='login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    trips       = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.start_date.desc()).limit(5).all()
    maintenance = Maintenance.query.filter_by(user_id=current_user.id).order_by(Maintenance.service_date.desc()).limit(5).all()
    expenses    = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.expense_date.desc()).limit(5).all()
    total_spend = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0
    return render_template('index.html', trips=trips, maintenance=maintenance, expenses=expenses, total_spend=total_spend)

@app.route('/trips')
@login_required
def trips():
    all_trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.start_date.desc()).all()
    return render_template('trips.html', trips=all_trips)

@app.route('/trips/new', methods=['GET', 'POST'])
@login_required
def new_trip():
    if request.method == 'POST':
        trip = Trip(
            user_id=current_user.id,
            title=request.form['title'],
            origin=request.form['origin'],
            destination=request.form['destination'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form.get('end_date') else None,
            distance_km=float(request.form['distance_km']) if request.form.get('distance_km') else None,
            notes=request.form.get('notes', '')
        )
        db.session.add(trip)
        db.session.commit()
        flash('Trip logged!', 'success')
        return redirect(url_for('trips'))
    return render_template('trip_detail.html', trip=None, mode='new')

@app.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('trips'))
    if request.method == 'POST':
        trip.title       = request.form['title']
        trip.origin      = request.form['origin']
        trip.destination = request.form['destination']
        trip.start_date  = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        trip.status      = request.form.get('status', trip.status)
        trip.notes       = request.form.get('notes', '')
        db.session.commit()
        flash('Trip updated.', 'success')
        return redirect(url_for('trips'))
    return render_template('trip_detail.html', trip=trip, mode='edit')

@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id == current_user.id:
        db.session.delete(trip)
        db.session.commit()
        flash('Trip deleted.', 'info')
    return redirect(url_for('trips'))

@app.route('/maintenance')
@login_required
def maintenance():
    logs = Maintenance.query.filter_by(user_id=current_user.id).order_by(Maintenance.service_date.desc()).all()
    return render_template('maintenance.html', logs=logs)

@app.route('/maintenance/new', methods=['POST'])
@login_required
def new_maintenance():
    log = Maintenance(
        user_id=current_user.id,
        service_type=request.form['service_type'],
        odometer_km=float(request.form['odometer_km']),
        service_date=datetime.strptime(request.form['service_date'], '%Y-%m-%d').date(),
        next_due_km=float(request.form['next_due_km']) if request.form.get('next_due_km') else None,
        cost=float(request.form.get('cost', 0)),
        workshop=request.form.get('workshop', ''),
        notes=request.form.get('notes', '')
    )
    db.session.add(log)
    db.session.commit()
    flash('Service log saved.', 'success')
    return redirect(url_for('maintenance'))

@app.route('/maintenance/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_maintenance(log_id):
    log = Maintenance.query.get_or_404(log_id)
    if log.user_id == current_user.id:
        db.session.delete(log)
        db.session.commit()
    return redirect(url_for('maintenance'))

@app.route('/expenses')
@login_required
def expenses():
    all_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.expense_date.desc()).all()
    trips        = Trip.query.filter_by(user_id=current_user.id).all()
    return render_template('expenses.html', expenses=all_expenses, trips=trips)

@app.route('/expenses/new', methods=['POST'])
@login_required
def new_expense():
    expense = Expense(
        user_id=current_user.id,
        trip_id=int(request.form['trip_id']) if request.form.get('trip_id') else None,
        category=request.form['category'],
        amount=float(request.form['amount']),
        currency=request.form.get('currency', 'NPR'),
        description=request.form.get('description', ''),
        expense_date=datetime.strptime(request.form['expense_date'], '%Y-%m-%d').date()
    )
    db.session.add(expense)
    db.session.commit()
    flash('Expense recorded.', 'success')
    return redirect(url_for('expenses'))

@app.route('/expenses/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for('expenses'))

if __name__ == '__main__':
    app.run(debug=True)