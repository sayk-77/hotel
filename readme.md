# Аннотация
Система управления гостиницей предназначена для автоматизации процессов бронирования и управления данными в гостинице. Программа позволяет сотрудникам просматривать записи о бронированиях, номерах и клиентах, а администраторам предоставляет возможность управлять этими данными. Основные функции включают управление бронированиями, номерами и клиентами.


# Введение
Основные возможности:
- Просмотр записей из разных таблиц
- Управление услугами
- Управление продажами
- Управление данными бронирований
- Управление данными номеров
- Управление данными клиентов
- Администрирование системы

# Назначение и условия применения
Данная программа предназначена для использования в гостиницах и отелях. Она помогает автоматизировать и упростить процесс управления гостиницей, улучшить обслуживание клиентов и повысить эффективность работы сотрудников.

# Установка
1. Клонируйте репозиторий:
```shell
git clone https://github.com/sayk-77/hotel.git
```
2. Перейдите в дирректорию с программой
```shell
cd hotel
```
3. Убедитесь, что Docker и Docker Compose установлены на вашем компьютере.
4. В консоль прописать следующую команду
```shell
docker-compose up
```
5. Откройте браузер и передите по следующему адресу
```shell
localhost:5000 или 127.0.0.1:5000
```

# Описание операций
- Просмотр записей сотрудников: Сотрудники могут просматривать все записи, связанные с их работой.
- Управление бронированиями: Администраторы могут добавлять, редактировать и удалять данные о бронированиях.
- Управление номерами: Администраторы могут управлять данными о номерах, включая добавление новых номеров и изменение информации о существующих.
- Управление клиентами: Администраторы могут управлять данными клиентов, включая контактную информацию и историю бронирований.
- Администрирование системы: Администраторы имеют доступ к настройкам системы и могут управлять пользователями и правами доступа.

# Термины и сокращения

| Термин         | Описание                                            |
|----------------|-----------------------------------------------------|
| Бронирование   | Процесс резервирования номера в гостинице           |
| Сотрудник      | Человек, работающий в гостинице и использующий систему |
| Администратор  | Человек, управляющий системой и данными              |
| Номер          | Жилое помещение в гостинице                         |
| Клиент         | Гость, использующий услуги гостиницы                |
| Система        | Программное обеспечение для управления гостиницей   |