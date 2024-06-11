from . import db

class EmployeeService(db.Model):
    __tablename__ = 'employees_services'
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)
    employee = db.relationship('Employee', backref=db.backref('employee_services', cascade="all, delete-orphan"))
    service = db.relationship('Service', backref=db.backref('employee_services', cascade="all, delete-orphan"))