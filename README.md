"#MotoLog" 

# MotoLog — Motorcycle Touring Management System

A web application built with Flask for motorcycle tourers to plan trips, track bike maintenance, and manage tour expenses.

## Features
- User registration and login with secure password hashing (Bcrypt)
- Role-based access control — Rider and Admin roles
- Admin dashboard to manage all users, trips, and expenses
- Trip planning and itinerary management
- Bike maintenance and service log tracking
- Expense tracker with category breakdown
- Fuel efficiency calculator
- Budget alert system
- Pre-ride checklist
- Responsive dark theme UI with Safety Orange accents

## Technologies Used
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Version Control:** Git, GitHub

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL Server
- Git

### Installation
1. Clone the repository:
git clone https://github.com/Promish-bista/motolog.git
cd motolog

2. Create and activate virtual environment: 
python -m venv venv
venv\Scripts\activate

3. Install dependencies: 
pip install -r requirements.txt     

4. Create a `.env` file in the root folder:
SECRET_KEY=your-secret-key
DB_USERNAME=root
DB_PASSWORD=your-mysql-password
DB_NAME=motolog_db
ADMIN_SECRET=your-admin-code

5. Create the MySQL database:
CREATE DATABASE motolog_db;

6. Run the application:
python app.py

7. Open your browser and go to `http://127.0.0.1:5000`

## Admin Access
To create an admin account, enter the admin secret code during registration.

## Video Demonstration
[Link will be added after recording]

## GitHub Repository
https://github.com/Promish-bista/motolog

## Module
ST5041CMD — The Internet and Web Technologies
Softwarica College of IT & E-Commerce in collaboration with Coventry University