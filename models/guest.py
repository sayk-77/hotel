from . import db

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_info = db.Column(db.String(100))
    country = db.Column(db.String(50))
    document = db.Column(db.String(50))
    check_in_out_date = db.Column(db.Date)
    bookings = db.relationship('Booking', backref='guest', lazy=True)