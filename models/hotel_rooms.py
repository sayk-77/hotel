from . import db

class HotelRooms(db.Model):
    __tablename__ = 'hotel_rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10))
    bookings = db.relationship('Booking', backref='room', lazy=True)
