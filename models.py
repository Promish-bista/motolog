from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bike_model    = db.Column(db.String(120), nullable=True)
    role          = db.Column(db.String(20),  default='rider', nullable=False)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    def is_admin(self):
        return self.role == 'admin'

class Trip(db.Model):
    __tablename__ = 'trips'
    id          = db.Column(db.Integer,     primary_key=True)
    user_id     = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    title       = db.Column(db.String(150), nullable=False)
    origin      = db.Column(db.String(150), nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    start_date  = db.Column(db.Date,        nullable=False)
    end_date    = db.Column(db.Date,        nullable=True)
    distance_km = db.Column(db.Float,       nullable=True)
    notes       = db.Column(db.Text,        nullable=True)
    status      = db.Column(db.String(20),  default='planned')
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)
    expenses    = db.relationship('Expense', backref='trip', lazy=True, cascade='all, delete-orphan')

class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    id           = db.Column(db.Integer,     primary_key=True)
    user_id      = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    odometer_km  = db.Column(db.Float,       nullable=False)
    service_date = db.Column(db.Date,        nullable=False)
    next_due_km  = db.Column(db.Float,       nullable=True)
    cost         = db.Column(db.Float,       default=0.0)
    workshop     = db.Column(db.String(150), nullable=True)
    notes        = db.Column(db.Text,        nullable=True)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow)

class Expense(db.Model):
    __tablename__ = 'expenses'
    id           = db.Column(db.Integer,     primary_key=True)
    user_id      = db.Column(db.Integer,     db.ForeignKey('users.id'), nullable=False)
    trip_id      = db.Column(db.Integer,     db.ForeignKey('trips.id'), nullable=True)
    category     = db.Column(db.String(50),  nullable=False)
    amount       = db.Column(db.Float,       nullable=False)
    currency     = db.Column(db.String(10),  default='NPR')
    description  = db.Column(db.String(255), nullable=True)
    expense_date = db.Column(db.Date,        nullable=False, default=datetime.utcnow)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow)