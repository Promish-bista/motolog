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
        log = Maintenance(
            user_id=user_id,
            service_type=form.get('service_type'),
            odometer_km=float(form.get('odometer_km')),
            service_date=datetime.strptime(form.get('service_date'), '%Y-%m-%d').date(),
            next_due_km=float(form.get('next_due_km')) if form.get('next_due_km') else None,
            cost=float(form.get('cost', 0)),
            workshop=form.get('workshop', ''),
            notes=form.get('notes', '')
        )
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def delete_log(log_id):
        log = Maintenance.query.get_or_404(log_id)
        db.session.delete(log)
        db.session.commit()