from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .employee import Employee
from .service import Service
from .guest import Guest
from .hotel_rooms import HotelRooms
from .booking import Booking
from .sale import Sale
from .employee_service import EmployeeService
from .user import User
from .role import Role
