# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from models import db, Service
# from flask_login import login_required, current_user
# from functools import wraps
#
# service_bp = Blueprint('service_bp', __name__)
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
# @service_bp.route('/services')
# @login_required
# def list_services():
#     services = Service.query.all()
#     return render_template('list_services.html', services=services)
#
# @service_bp.route('/add_service', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def add_service():
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         new_service = Service(name=name, description=description)
#         db.session.add(new_service)
#         db.session.commit()
#         flash('Услуга успешно добавлена!', 'success')
#         return redirect(url_for('service_bp.list_services'))
#     return render_template('add_service.html')
#
# @service_bp.route('/edit_service/<int:id>', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def edit_service(id):
#     service = Service.query.get_or_404(id)
#     if request.method == 'POST':
#         service.name = request.form['name']
#         service.description = request.form['description']
#         db.session.commit()
#         flash('Услуга успешно обновлена!', 'success')
#         return redirect(url_for('service_bp.list_services'))
#     return render_template('edit_service.html', service=service)
#
# @service_bp.route('/delete_service/<int:id>', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def delete_service(id):
#     service = Service.query.get_or_404(id)
#     if request.method == 'POST':
#         db.session.delete(service)
#         db.session.commit()
#         flash('Услуга успешно удалена!', 'success')
#         return redirect(url_for('service_bp.list_services'))
#     return render_template('delete_service.html', service=service)
