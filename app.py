from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_file
from sqlalchemy import or_

from config import Config
from models import db, Employee, Service, Guest, HotelRooms, Booking, Sale, EmployeeService, User, Role
import pandas as pd

from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps

from names import column_names

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Пожалуйста, войдите, чтобы получить доступ к этой странице.', 'warning')
    return redirect(url_for('login'))


def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role.name != role:
                flash('У вас нет доступа к этому ресурсу.', 'error')
                return redirect(request.referrer or url_for('index'))
            return f(*args, **kwargs)

        return decorated_function

    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        hire_date = request.form['hire_date']
        salary = request.form['salary']
        contact_info = request.form['contact_info']
        new_employee = Employee(first_name=first_name, last_name=last_name, position=position, hire_date=hire_date,
                                salary=salary, contact_info=contact_info)
        db.session.add(new_employee)
        db.session.commit()
        flash('Сотрудник успешно добавлен!', 'success')
        return redirect(url_for('index'))
    return render_template('add_employee.html')


@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.first_name = request.form['first_name']
        employee.last_name = request.form['last_name']
        employee.position = request.form['position']
        employee.hire_date = request.form['hire_date']
        employee.salary = request.form['salary']
        employee.contact_info = request.form['contact_info']
        db.session.commit()
        flash('Сотрудник успешно обновлен!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_employee.html', employee=employee)


@app.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        EmployeeService.query.filter_by(employee_id=id).delete()
        db.session.delete(employee)
        db.session.commit()
        flash('Сотрудник успешно удален!', 'success')
        return redirect(url_for('index'))
    return render_template('delete_employee.html', employee=employee)


@app.template_filter('getattr')
def getattr_filter(obj, name):
    return getattr(obj, name)


def create_search_query(model, search_query):
    columns = model.__table__.columns
    filters = [column.contains(search_query) for column in columns if column.type.python_type == str]
    return model.query.filter(or_(*filters)).all()


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    results = []
    columns = []
    table_name = ""

    if request.method == 'POST':
        search_query = request.form['query']
        table = request.form['table']
        table_name = table

        if table == 'employees':
            results = create_search_query(Employee, search_query)
            columns = [column.name for column in Employee.__table__.columns]
        elif table == 'guests':
            results = create_search_query(Guest, search_query)
            columns = [column.name for column in Guest.__table__.columns]
        elif table == 'services':
            results = create_search_query(Service, search_query)
            columns = [column.name for column in Service.__table__.columns]
        elif table == 'bookings':
            results = create_search_query(Booking, search_query)
            columns = [column.name for column in Booking.__table__.columns]
        elif table == 'employee_services':
            results = create_search_query(EmployeeService, search_query)
            columns = [column.name for column in EmployeeService.__table__.columns]
        elif table == 'hotel_rooms':
            results = create_search_query(HotelRooms, search_query)
            columns = [column.name for column in HotelRooms.__table__.columns]
        elif table == 'roles':
            results = create_search_query(Role, search_query)
            columns = [column.name for column in Role.__table__.columns]
        elif table == 'sales':
            results = create_search_query(Sale, search_query)
            columns = [column.name for column in Sale.__table__.columns]
        elif table == 'users':
            results = create_search_query(User, search_query)
            columns = [column.name for column in User.__table__.columns]

    return render_template('search_result.html', results=results, columns=columns, column_names=column_names,
                           table_name=table_name)


def dataframe_to_csv_response(df, filename):
    csv_data = df.to_csv(index=False, encoding='utf-8')
    response = app.response_class(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename={filename}'}
    )
    return response

@app.route('/sales')
@login_required
def sales_list():
    sales = Sale.query.all()
    return render_template('sales.html', sales=sales)


@app.route('/edit_sale/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)

    if request.method == 'POST':
        sale.transaction_id = request.form['transaction_id']
        sale.sale_date = request.form['sale_date']
        sale.guest_id = request.form['guest_id']
        sale.sale_amount = request.form['sale_amount']
        sale.payment_method = request.form['payment_method']
        db.session.commit()
        flash("Данные успещно обновлены")
        return redirect(url_for('sales_list'))

    guests = Guest.query.all()
    return render_template('edit_sale.html', sale=sale, guests=guests)

@app.route('/delete_sale/<int:sale_id>', methods=['GET'])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash("Продажа успешно удалена")
    return render_template('base.html')


from flask import render_template, redirect, url_for, request


@app.route('/add_sale', methods=['GET', 'POST'])
@login_required
def add_sale():
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        sale_date = request.form['sale_date']
        guest_id = request.form['guest_id']
        sale_amount = request.form['sale_amount']
        payment_method = request.form['payment_method']

        new_sale = Sale(transaction_id=transaction_id, sale_date=sale_date,
                        guest_id=guest_id, sale_amount=sale_amount,
                        payment_method=payment_method)

        db.session.add(new_sale)
        db.session.commit()

        return redirect(url_for('sales_list'))

    guests = Guest.query.all()
    return render_template('add_sale.html', guests=guests)


@app.route('/export_csv', methods=['POST', 'GET'])
@login_required
def export_csv():
    if request.method == 'POST':
        data_dict = request.form.to_dict(flat=False)
        columns = data_dict['columns'][0].split(',')
        results = [data_dict[f'results[{i}]'] for i in range(len(columns))]

        df = pd.DataFrame(results).transpose()
        df.columns = columns

        df.to_csv('export.csv', index=False)

        return send_file('export.csv', as_attachment=True)

    return render_template('export_select.html')


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_name = request.form['role']
        role = Role.query.filter_by(name=role_name).first()
        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь успешно добавлен!', 'success')
        return redirect(url_for('index'))
    roles = Role.query.all()
    return render_template('add_user.html', roles=roles)


@app.route('/users')
@login_required
@role_required('admin')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)


@app.route('/delete_user/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('list_users'))


@app.route('/guests')
@login_required
def list_guests():
    guests = Guest.query.all()
    return render_template('list_guests.html', guests=guests)


@app.route('/add_guest', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_guest():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_info = request.form['contact_info']
        country = request.form['country']
        id_document = request.form['id_document']
        check_in_out_date = request.form['check_in_out_date']
        new_guest = Guest(first_name=first_name, last_name=last_name, contact_info=contact_info, country=country,
                          id_document=id_document, check_in_out_date=check_in_out_date)
        db.session.add(new_guest)
        db.session.commit()
        flash('Гость успешно добавлен!', 'success')
        return redirect(url_for('list_guests'))
    return render_template('add_guest.html')


@app.route('/edit_guest/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_guest(id):
    guest = Guest.query.get_or_404(id)
    if request.method == 'POST':
        guest.first_name = request.form['first_name']
        guest.last_name = request.form['last_name']
        guest.contact_info = request.form['contact_info']
        guest.country = request.form['country']
        guest.id_document = request.form['id_document']
        guest.check_in_out_date = request.form['check_in_out_date']
        db.session.commit()
        flash('Гость успешно обновлен!', 'success')
        return redirect(url_for('list_guests'))
    return render_template('edit_guest.html', guest=guest)


@app.route('/delete_guest/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_guest(id):
    guest = Guest.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(guest)
        db.session.commit()
        flash('Гость успешно удален!', 'success')
        return redirect(url_for('list_guests'))
    return render_template('delete_guest.html', guest=guest)


@app.route('/services')
@login_required
def list_services():
    services = Service.query.all()
    return render_template('list_services.html', services=services)


@app.route('/add_service', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_service():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_service = Service(name=name, description=description)
        db.session.add(new_service)
        db.session.commit()
        flash('Услуга успешно добавлена!', 'success')
        return redirect(url_for('list_services'))
    return render_template('add_services.html')


@app.route('/edit_service/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_service(id):
    service = Service.query.get_or_404(id)
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        db.session.commit()
        flash('Услуга успешно обновлена!', 'success')
        return redirect(url_for('list_services'))
    return render_template('edit_services.html', service=service)


@app.route('/delete_service/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_service(id):
    service = Service.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(service)
        db.session.commit()
        flash('Услуга успешно удалена!', 'success')
        return redirect(url_for('list_services'))
    return render_template('delete_services.html', service=service)


@app.route('/bookings')
@login_required
def list_bookings():
    bookings = Booking.query.all()
    return render_template('list_booking.html', bookings=bookings)


@app.route('/add_booking', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_booking():
    if request.method == 'POST':
        booking_number = request.form['booking_number']
        booking_date = request.form['booking_date']
        guest_id = request.form['guest_id']
        room_id = request.form['room_id']
        new_booking = Booking(booking_number=booking_number, booking_date=booking_date, guest_id=guest_id,
                              room_id=room_id)
        db.session.add(new_booking)
        db.session.commit()
        flash('Бронирование успешно добавлено!', 'success')
        return redirect(url_for('list_bookings'))
    guests = Guest.query.all()
    rooms = HotelRooms.query.all()
    return render_template('add_booking.html', guests=guests, rooms=rooms)


@app.route('/edit_booking/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_booking(id):
    booking = Booking.query.get_or_404(id)
    if request.method == 'POST':
        booking.booking_number = request.form['booking_number']
        booking.booking_date = request.form['booking_date']
        booking.guest_id = request.form['guest_id']
        booking.room_id = request.form['room_id']
        db.session.commit()
        flash('Бронирование успешно обновлено!', 'success')
        return redirect(url_for('list_bookings'))
    guests = Guest.query.all()
    rooms = HotelRooms.query.all()
    return render_template('edit_booking.html', booking=booking, guests=guests, rooms=rooms)


@app.route('/delete_booking/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(booking)
        db.session.commit()
        flash('Бронирование успешно удалено!', 'success')
        return redirect(url_for('list_bookings'))
    return render_template('delete_booking.html', booking=booking)


@app.route('/employee_services')
@login_required
def list_employee_services():
    employee_services = EmployeeService.query.all()
    return render_template('list_employee_services.html', employee_services=employee_services)


@app.route('/add_employee_service', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_employee_service():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        service_id = request.form['service_id']
        new_employee_service = EmployeeService(employee_id=employee_id, service_id=service_id)
        db.session.add(new_employee_service)
        db.session.commit()
        flash('История услуги добавлена!', 'success')
        return redirect(url_for('list_employee_services'))
    employees = Employee.query.all()
    services = Service.query.all()
    return render_template('add_employee_services.html', employees=employees, services=services)


@app.route('/edit_employee_service/<int:employee_id>/<int:service_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_employee_service(employee_id, service_id):
    employee_service = EmployeeService.query.get((employee_id, service_id))
    if request.method == 'POST':
        employee_service.employee_id = request.form['employee_id']
        employee_service.service_id = request.form['service_id']
        db.session.commit()
        flash('История услуг успегно изменена!', 'success')
        return redirect(url_for('list_employee_services'))
    employees = Employee.query.all()
    services = Service.query.all()
    return render_template('edit_employee_services.html', employee_service=employee_service, employees=employees,
                           services=services)


@app.route('/delete_employee_service/<int:employee_id>/<int:service_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_employee_service(employee_id, service_id):
    employee_service = EmployeeService.query.get((employee_id, service_id))
    if request.method == 'POST':
        db.session.delete(employee_service)
        db.session.commit()
        flash('История услуг успешно удалена!', 'success')
        return redirect(url_for('list_employee_services'))
    return render_template('delete_employee_services.html', employee_service=employee_service)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="192.168.0.105", port=5000)
