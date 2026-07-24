from models import db, Maintenance
from datetime import datetime

class MaintenanceController:

    @staticmethod
    def get_user_logs(user_id):
        return Maintenance.query.filter_by(user_id=user_id).order_by(Maintenance.service_date.desc()).all()

    @staticmethod
    def get_all_logs():
        return Maintenance.query.order_by(Maintenance.service_date.desc()).all()

    @staticmethod
    def create_log(user_id, form):
        service_type = form.get('service_type', '').strip()
        odometer_km  = form.get('odometer_km', '').strip()
        service_date = form.get('service_date', '').strip()

        if not service_type or not odometer_km or not service_date:
            return None, 'Please fill in all required fields.'

        try:
            odometer_km = float(odometer_km)
            if odometer_km < 0:
                return None, 'Odometer reading cannot be negative.'
        except ValueError:
            return None, 'Invalid odometer value.'

        try:
            service_date = datetime.strptime(service_date, '%Y-%m-%d').date()
        except ValueError:
            return None, 'Invalid date format.'

        next_due_km = None
        if form.get('next_due_km'):
            try:
                next_due_km = float(form.get('next_due_km'))
                if next_due_km <= odometer_km:
                    return None, 'Next due km must be greater than current odometer reading.'
            except ValueError:
                return None, 'Invalid next due km value.'

        cost = 0.0
        if form.get('cost'):
            try:
                cost = float(form.get('cost'))
                if cost < 0:
                    return None, 'Cost cannot be negative.'
            except ValueError:
                return None, 'Invalid cost value.'

        log = Maintenance(
            user_id=user_id,
            service_type=service_type,
            odometer_km=odometer_km,
            service_date=service_date,
            next_due_km=next_due_km,
            cost=cost,
            workshop=form.get('workshop', '').strip(),
            notes=form.get('notes', '').strip()
        )
        db.session.add(log)
        db.session.commit()
        return log, None

    @staticmethod
    def delete_log(log_id, user_id=None):
        query = Maintenance.query.filter_by(id=log_id)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        log = query.first_or_404()
        db.session.delete(log)
        db.session.commit()
