from . import db

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50))
    sale_date = db.Column(db.Date)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    sale_amount = db.Column(db.Numeric)
    payment_method = db.Column(db.String(50))
