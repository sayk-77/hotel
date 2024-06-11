from . import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(50))
    booking_date = db.Column(db.Date)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('hotel_rooms.id'), nullable=False)

