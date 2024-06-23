from app import app, db, User, Role

with app.app_context():
    admin_role = Role.query.filter_by(name='admin').first()
    employee_role = Role.query.filter_by(name='employee').first()

    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)

    if not employee_role:
        employee_role = Role(name='employee')
        db.session.add(employee_role)

    admin = User(username='admin', role=admin_role)
    admin.set_password('adminpassword')
    db.session.add(admin)

    employee = User(username='employee', role=employee_role)
    employee.set_password('employeepassword')
    db.session.add(employee)

    db.session.commit()
    print("Admin and employee users created successfully.")
