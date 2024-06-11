column_names = {
    'bookings': {
        'id': 'ID',
        'booking_number': 'Номер бронирования',
        'booking_date': 'Дата бронирования',
        'guest_id': 'ID гостя',
        'room_id': 'ID комнаты'
    },
    'employees': {
        'id': 'ID',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'position': 'Должность',
        'hire_date': 'Дата найма',
        'salary': 'Зарплата',
        'contact_info': 'Контактная информация'
    },
    'employee_services': {
        'employee_id': 'ID сотрудника',
        'service_id': 'ID услуги'
    },
    'guests': {
        'id': 'ID',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'contact_info': 'Контактная информация',
        'country': 'Страна',
        'document': 'Документ',
        'check_in_out_date': 'Дата заезда/выезда'
    },
    'hotel_rooms': {
        'id': 'ID',
        'room_number': 'Номер комнаты'
    },
    'roles': {
        'id': 'ID',
        'name': 'Название роли'
    },
    'sales': {
        'id': 'ID',
        'transaction_id': 'ID транзакции',
        'sale_date': 'Дата продажи',
        'guest_id': 'ID гостя',
        'sale_amount': 'Сумма продажи',
        'payment_method': 'Метод оплаты'
    },
    'services': {
        'id': 'ID',
        'name': 'Название услуги',
        'description': 'Описание'
    },
    'users': {
        'id': 'ID',
        'username': 'Имя пользователя',
        'password_hash': 'Хэш пароля',
        'role_id': 'ID роли'
    }
}
