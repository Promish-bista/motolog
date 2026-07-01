from models import db, Expense
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
        expense = Expense(
            user_id=user_id,
            trip_id=int(form.get('trip_id')) if form.get('trip_id') else None,
            category=form.get('category'),
            amount=float(form.get('amount')),
            currency=form.get('currency', 'NPR'),
            description=form.get('description', ''),
            expense_date=datetime.strptime(form.get('expense_date'), '%Y-%m-%d').date()
        )
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def delete_expense(expense_id):
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()

    @staticmethod
    def get_total_spend(user_id):
        from sqlalchemy import func
        total = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar()
        return total or 0