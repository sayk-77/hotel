# from flask import Blueprint, render_template, request, redirect, url_for, flash
# import pandas as pd
# from models import Employee, Guest, Service, Booking, EmployeeService
#
# export_bp = Blueprint('export_bp', __name__)
#
# def dataframe_to_csv_response(df, filename):
#     csv_data = df.to_csv(index=False, encoding='utf-8')
#     response = app.response_class(
#         csv_data,
#         mimetype='text/csv',
#         headers={'Content-Disposition': f'attachment;filename={filename}'}
#     )
#     return response
#
# @export_bp.route('/export_csv', methods=['GET', 'POST'])
# @login_required
# def export_csv():
#     if request.method == 'POST':
#         table_name = request.form['table']
#         if table_name == 'employees':
#             employees = Employee.query.all()
#             data = [{"ID": emp.id, "FirstName": emp.first_name, "LastName": emp.last_name, "Position": emp.position, "HireDate": emp.hire_date, "Salary": emp.salary, "ContactInfo": emp.contact_info} for emp in employees]
#             df = pd.DataFrame(data)
#             return dataframe_to_csv_response(df, 'employees.csv')
#         elif table_name == 'guests':
#             guests = Guest.query.all()
#             data = [{"ID": guest.id, "FirstName": guest.first_name, "LastName": guest.last_name, "ContactInfo": guest.contact_info, "Country": guest.country, "IDDocument": guest.id_document, "CheckInOutDate": guest.check_in_out_date} for guest in guests]
#             df = pd.DataFrame(data)
#             return dataframe_to_csv_response(df, 'guests.csv')
#         elif table_name == 'services':
#             services = Service.query.all()
#             data = [{"ID": service.id, "Name": service.name, "Description": service.description} for service in services]
#             df = pd.DataFrame(data)
#             return dataframe_to_csv_response(df, 'services.csv')
#         elif table_name == 'bookings':
#             bookings = Booking.query.all()
#             data = [{"ID": booking.id, "BookingNumber": booking.booking_number, "BookingDate": booking.booking_date, "GuestID": booking.guest_id, "RoomID": booking.room_id} for booking in bookings]
#             df = pd.DataFrame(data)
#             return dataframe_to_csv_response(df, 'bookings.csv')
#         elif table_name == 'employee_services':
#             employee_services = EmployeeService.query.all()
#             data = [{"EmployeeID": es.employee_id, "ServiceID": es.service_id} for es in employee_services]
#             df = pd.DataFrame(data)
#             return dataframe_to_csv_response(df, 'employee_services.csv')
#         else:
#             flash('Неверное название таблицы', 'error')
#             return redirect(url_for('export_bp.export_csv'))
#     return render_template('export_select.html')
