# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from models import db, Employee, EmployeeService
# from flask_login import login_required, current_user
# from functools import wraps
#
# employee_bp = Blueprint('employee_bp', __name__)
#
# def role_required(role):
#     def wrapper(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if current_user.role.name != role:
#                 flash('У вас нет доступа к этому ресурсу.', 'error')
#                 return redirect(url_for('index'))
#             return f(*args, **kwargs)
#         return decorated_function
#     return wrapper
#
# @employee_bp.route('/')
# @login_required
# def index():
#     employees = Employee.query.all()
#     return render_template('index.html', employees=employees)
#
# @employee_bp.route('/add_employee', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def add_employee():
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         position = request.form['position']
#         hire_date = request.form['hire_date']
#         salary = request.form['salary']
#         contact_info = request.form['contact_info']
#         new_employee = Employee(first_name=first_name, last_name=last_name, position=position, hire_date=hire_date, salary=salary, contact_info=contact_info)
#         db.session.add(new_employee)
#         db.session.commit()
#         flash('Сотрудник успешно добавлен!', 'success')
#         return redirect(url_for('employee_bp.index'))
#     return render_template('add_employee.html')
#
# @employee_bp.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def edit_employee(id):
#     employee = Employee.query.get_or_404(id)
#     if request.method == 'POST':
#         employee.first_name = request.form['first_name']
#         employee.last_name = request.form['last_name']
#         employee.position = request.form['position']
#         employee.hire_date = request.form['hire_date']
#         employee.salary = request.form['salary']
#         employee.contact_info = request.form['contact_info']
#         db.session.commit()
#         flash('Сотрудник успешно обновлен!', 'success')
#         return redirect(url_for('employee_bp.index'))
#     return render_template('edit_employee.html', employee=employee)
#
# @employee_bp.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def delete_employee(id):
#     employee = Employee.query.get_or_404(id)
#     if request.method == 'POST':
#         EmployeeService.query.filter_by(employee_id=id).delete()
#         db.session.delete(employee)
#         db.session.commit()
#         flash('Сотрудник успешно удален!', 'success')
#         return redirect(url_for('employee_bp.index'))
#     return render_template('delete_employee.html', employee=employee)
