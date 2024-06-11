from . import db

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    hire_date = db.Column(db.Date)
    salary = db.Column(db.Numeric)
    contact_info = db.Column(db.String(100))
