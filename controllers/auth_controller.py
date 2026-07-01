from models import db, User
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt()

class AuthController:

    @staticmethod
    def register_user(username, email, password, bike_model, admin_code):
        existing = User.query.filter_by(email=email).first()
        if existing:
            return None, 'Email already registered.'

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return None, 'Username already taken.'

        role = 'rider'
        if admin_code and admin_code == os.getenv('ADMIN_SECRET'):
            role = 'admin'

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            username=username,
            email=email,
            password_hash=hashed_pw,
            bike_model=bike_model,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def login_user_check(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def get_all_users():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()