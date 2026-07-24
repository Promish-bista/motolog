from models import db, Expense, Trip
from datetime import datetime

class ExpenseController:

    @staticmethod
    def get_user_expenses(user_id):
        return Expense.query.filter_by(user_id=user_id).order_by(Expense.expense_date.desc()).all()

    @staticmethod
    def get_all_expenses():
        return Expense.query.order_by(Expense.expense_date.desc()).all()

    @staticmethod
    def create_expense(user_id, form):
        category     = form.get('category', '').strip()
        amount       = form.get('amount', '').strip()
        expense_date = form.get('expense_date', '').strip()

        if not category or not amount or not expense_date:
            return None, 'Please fill in all required fields.'

        try:
            amount = float(amount)
            if amount <= 0:
                return None, 'Amount must be greater than zero.'
        except ValueError:
            return None, 'Invalid amount value.'

        try:
            expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()
        except ValueError:
            return None, 'Invalid date format.'

        trip_id = None
        if form.get('trip_id'):
            try:
                trip_id = int(form.get('trip_id'))
            except (TypeError, ValueError):
                return None, 'Invalid trip selected.'
            if not Trip.query.filter_by(id=trip_id, user_id=user_id).first():
                return None, 'You can only link expenses to your own trips.'

        expense = Expense(
            user_id=user_id,
            trip_id=trip_id,
            category=category,
            amount=amount,
            currency=form.get('currency', 'NPR'),
            description=form.get('description', '').strip(),
            expense_date=expense_date
        )
        db.session.add(expense)
        db.session.commit()
        return expense, None

    @staticmethod
    def delete_expense(expense_id, user_id=None):
        query = Expense.query.filter_by(id=expense_id)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        expense = query.first_or_404()
        db.session.delete(expense)
        db.session.commit()

    @staticmethod
    def get_total_spend(user_id):
        from sqlalchemy import func
        total = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar()
        return total or 0
