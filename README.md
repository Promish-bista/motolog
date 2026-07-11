# MotoLog — Motorcycle Touring Management System

A full-stack web application built with Flask and MySQL for motorcycle tourers to plan trips, track bike maintenance, and manage tour expenses securely.



## GitHub Repository
https://github.com/Promish-bista/motolog


## Features

### Rider Features
Secure registration and login with Bcrypt password hashing
Personal dashboard with trip summary, service reminder, fuel calculator, and budget monitor
Trip planning — log routes with origin, destination, dates, distance, and status
Inline trip status update (planned → active → completed) directly from trips list
Live search and filter on trips and expenses
Bike maintenance log with next service due reminder
Expense tracker with category breakdown (fuel, food, accommodation, gear, misc)
Budget alert system — warns at 80% of set limit
Pre-ride safety checklist (8 items, local state)
Profile page with username, bike model, and password update

### Admin Features
Separate admin dashboard (role-based access control)
View and manage all registered riders
View and delete all trips, expenses, and service logs platform-wide
Search functionality across users and trips
Admin account created via secret registration code

### Security Features
Bcrypt password hashing (never stores plain text)
SQL injection protection via SQLAlchemy ORM
Role-based access control with custom `@role_required` decorator
Session cookie security (HttpOnly, SameSite)
Environment variables for sensitive config (SECRET_KEY, DB credentials)
Admin secret code for privileged account creation



## Technologies Used
 Layer : Technology 

Backend : Python 3.13, Flask 3.1
Database : MySQL 8.0, Flask-SQLAlchemy
Authentication : Flask-Login, Flask-Bcrypt
Frontend : HTML5, CSS3, JavaScript (vanilla)
Templates : Jinja2 
Version Control : Git, GitHub 

---

## Project Structure
motolog/
├── app.py                  # Flask routes and app factory
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── TESTING.md              # Manual test cases (32 tests)
├── CHANGELOG.md            # Version history
├── controllers/
│   ├── auth_controller.py
│   ├── trip_controller.py
│   ├── maintenance_controller.py
│   └── expense_controller.py
├── utils/
│   └── decorators.py       # @role_required decorator
├── static/
│   ├── css/style.css       # Dark theme with CSS variables
│   └── js/calculations.js  # Fuel calc, budget alerts, checklist
└── templates/
├── base.html
├── index.html          # Rider dashboard
├── admin_dashboard.html
├── login.html
├── trips.html
├── trip_detail.html
├── maintenance.html
├── expenses.html
├── profile.html
└── 404.html