from sqlalchemy import and_
from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, \
    raiseload, noload

from department_app import db
from department_app.models.employee import Employee


class EmployeeService:
    strategies = {
        lazyload, joinedload, subqueryload, selectinload, raiseload, noload
    }

    @classmethod
    def get_employees(cls, strategy=lazyload):
        cls.__check_strategy(strategy)

        return db.session.query(Employee).options(
            strategy(Employee.department)
        ).all()

    @staticmethod
    def get_employee_by_uuid(uuid):
        employee = db.session.query(Employee).filter_by(uuid=uuid).first()
        if employee is None:
            raise ValueError('Invalid employee uuid')
        return employee

    @staticmethod
    def add_employee(schema, employee_json):
        employee = schema.load(employee_json, session=db.session)
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def update_employee(cls, schema, uuid, employee_json):
        employee = cls.get_employee_by_uuid(uuid)
        if employee is None:
            raise ValueError('Invalid employee uuid')
        employee = schema.load(
            employee_json, session=db.session, instance=employee
        )
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def delete_employee(cls, uuid):
        employee = cls.get_employee_by_uuid(uuid)
        if employee is None:
            raise ValueError('Invalid employee uuid')
        db.session.delete(employee)
        db.session.commit()

    @classmethod
    def get_employees_by_date_of_birth(cls, date, strategy=lazyload):
        cls.__check_strategy(strategy)

        employees = db.session.query(Employee).filter_by(
            date_of_birth=date
        ).all()
        if employees is None:
            raise ValueError(f'Employee born on date {date} not found')
        return employees

    @classmethod
    def get_employees_born_in_period(cls, start_date, end_date,
                                     strategy=lazyload):
        cls.__check_strategy(strategy)

        employees = db.session.query(Employee).filter(
            and_(
                Employee.date_of_birth > start_date,
                Employee.date_of_birth < end_date
            )
        ).all()
        if employees is None:
            raise ValueError(
                f'Employee born between {start_date} and {end_date} not found'
            )
        return employees

    @classmethod
    def __check_strategy(cls, strategy):
        if strategy not in cls.strategies:
            raise ValueError(
                f'Unsupported strategy. Only {cls.strategies} are allowed')
