from datetime import date

from department_app import db
from department_app.models.department import Department
from department_app.models.employee import Employee


def populate_database():
    department_1 = Department('Research and Development', 'Google')
    department_2 = Department('Purchasing', 'Amazon')
    department_3 = Department('Human Resource Management', 'Huawei')

    employee_1 = Employee('John Doe', date(1996, 5, 12), 2000)
    employee_2 = Employee('Jane Wilson', date(1993, 2, 23), 2100)
    employee_3 = Employee('Will Hunting', date(1989, 11, 30), 1800)

    department_1.employees = [employee_1]
    department_2.employees = [employee_2]
    department_3.employees = [employee_3]

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating database...')
    populate_database()
    print('Successfully populated')
