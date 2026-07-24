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
        title       = form.get('title', '').strip()
        origin      = form.get('origin', '').strip()
        destination = form.get('destination', '').strip()
        start_date  = form.get('start_date', '').strip()

        if not title or not origin or not destination or not start_date:
            return None, 'Please fill in all required fields.'

        if len(title) > 150:
            return None, 'Trip name must be under 150 characters.'

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date   = datetime.strptime(form.get('end_date'), '%Y-%m-%d').date() if form.get('end_date') else None
            if end_date and end_date < start_date:
                return None, 'End date cannot be before start date.'
        except ValueError:
            return None, 'Invalid date format.'

        distance_km = None
        if form.get('distance_km'):
            try:
                distance_km = float(form.get('distance_km'))
                if distance_km < 0:
                    return None, 'Distance cannot be negative.'
            except ValueError:
                return None, 'Invalid distance value.'

        trip = Trip(
            user_id=user_id,
            title=title,
            origin=origin,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            distance_km=distance_km,
            notes=form.get('notes', '').strip()
        )
        db.session.add(trip)
        db.session.commit()
        return trip, None

    @staticmethod
    def update_trip(trip_id, form):
        trip = Trip.query.get_or_404(trip_id)
        title = form.get('title', '').strip()
        origin = form.get('origin', '').strip()
        destination = form.get('destination', '').strip()
        if not title or not origin or not destination:
            return None, 'Please fill in all required fields.'
        if len(title) > 150:
            return None, 'Trip name must be under 150 characters.'

        end_date_value = form.get('end_date')
        try:
            start_date = datetime.strptime(form.get('start_date', ''), '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_value, '%Y-%m-%d').date() if end_date_value else None
        except ValueError:
            return None, 'Invalid date format.'
        if 'end_date' not in form:
            end_date = trip.end_date
        if end_date and end_date < start_date:
            return None, 'End date cannot be before start date.'

        distance_km = trip.distance_km
        if 'distance_km' in form and not form.get('distance_km'):
            distance_km = None
        elif form.get('distance_km'):
            try:
                distance_km = float(form.get('distance_km'))
            except ValueError:
                return None, 'Invalid distance value.'
            if distance_km < 0:
                return None, 'Distance cannot be negative.'

        status = form.get('status', trip.status)
        if status not in {'planned', 'active', 'completed'}:
            return None, 'Invalid trip status.'

        trip.title       = title
        trip.origin      = origin
        trip.destination = destination
        trip.start_date  = start_date
        trip.end_date    = end_date
        trip.distance_km = distance_km
        trip.status      = status
        trip.notes       = form.get('notes', '').strip()
        db.session.commit()
        return trip, None

    @staticmethod
    def delete_trip(trip_id):
        trip = Trip.query.get_or_404(trip_id)
        db.session.delete(trip)
        db.session.commit()
