from models import db, Trip
from datetime import datetime

class TripController:

    @staticmethod
    def get_user_trips(user_id):
        return Trip.query.filter_by(user_id=user_id).order_by(Trip.start_date.desc()).all()

    @staticmethod
    def get_all_trips():
        return Trip.query.order_by(Trip.start_date.desc()).all()

    @staticmethod
    def get_trip_by_id(trip_id):
        return Trip.query.get_or_404(trip_id)

    @staticmethod
    def create_trip(user_id, form):
        trip = Trip(
            user_id=user_id,
            title=form.get('title'),
            origin=form.get('origin'),
            destination=form.get('destination'),
            start_date=datetime.strptime(form.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(form.get('end_date'), '%Y-%m-%d').date() if form.get('end_date') else None,
            distance_km=float(form.get('distance_km')) if form.get('distance_km') else None,
            notes=form.get('notes', '')
        )
        db.session.add(trip)
        db.session.commit()
        return trip

    @staticmethod
    def update_trip(trip_id, form):
        trip = Trip.query.get_or_404(trip_id)
        trip.title       = form.get('title')
        trip.origin      = form.get('origin')
        trip.destination = form.get('destination')
        trip.start_date  = datetime.strptime(form.get('start_date'), '%Y-%m-%d').date()
        trip.status      = form.get('status', trip.status)
        trip.notes       = form.get('notes', '')
        db.session.commit()
        return trip

    @staticmethod
    def delete_trip(trip_id):
        trip = Trip.query.get_or_404(trip_id)
        db.session.delete(trip)
        db.session.commit()