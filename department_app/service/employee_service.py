"""
Employee service used to make database queries, this module defines the
following classes:

- `EmployeeService`, employee service
"""
# pylint: disable=cyclic-import

from sqlalchemy import and_
from sqlalchemy.orm import lazyload

from department_app import db
from department_app.models.employee import Employee
from department_app.service.strategized_service import StrategizedService


class EmployeeService(StrategizedService):
    """
    Employee service used to make database queries
    """
    @classmethod
    def get_employees(cls, strategy=lazyload):
        """
       Fetches all of the employees from database using given strategy

       :param strategy: loading strategy to be used for nested fields
       :return: list of all employees
       """
        cls._check_strategy(strategy)

        return db.session.query(Employee).options(
            strategy(Employee.department)
        ).all()

    @staticmethod
    def get_employee_by_uuid(uuid):
        """
        Fetches the employee with given UUID from database, raises
        ValueError if such employee is not found

        :param uuid: UUID of the employee to be fetched
        :raise ValueError: in case of employee with given UUID being absent
        in the database
        :return: employee with given UUID
        """
        employee = db.session.query(Employee).filter_by(uuid=uuid).first()
        if employee is None:
            raise ValueError('Invalid employee uuid')
        return employee

    @staticmethod
    def add_employee(schema, employee_json):
        """
        Deserializes employee and adds it to the database

        :param schema: schema to be used to deserialize the employee
        :param employee_json: data to deserialize the employee from
        :return: employee that was added
        """
        employee = schema.load(employee_json, session=db.session)
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def update_employee(cls, schema, uuid, employee_json):
        """
        Deserializes employee and updates employee with given UUID using
        latter, raises ValueError if employee with given UUID is not found

        :param schema: schema to be used to deserialize the employee
        :param uuid: UUID of the employee to be updated
        :param employee_json: data to deserialize the employee from
        :raise ValueError: in case of employee with given UUID being absent
        in the database
        :return: employee that was updated
        """
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
        """
        Deletes the employee with given UUID from database, raises
        ValueError if such employee is not found

        :param uuid: UUID of the employee to be deleted
        :raise ValueError: in case of employee with given UUID being absent
        in the database
        :return: None
        """
        employee = cls.get_employee_by_uuid(uuid)
        if employee is None:
            raise ValueError('Invalid employee uuid')
        db.session.delete(employee)
        db.session.commit()

    @classmethod
    def get_employees_by_date_of_birth(cls, date, strategy=lazyload):
        """
        Fetches employees born on given date from database

        :param date: date of birth of employees to be fetched
        :param strategy: loading strategy to be used for nested fields
        :return: employee born on given date
        """
        cls._check_strategy(strategy)

        employees = db.session.query(Employee).options(
            strategy(Employee.department)
        ).filter_by(
            date_of_birth=date
        ).all()
        return employees

    @classmethod
    def get_employees_born_in_period(cls, start_date, end_date,
                                     strategy=lazyload):
        """
        Fetches employees born in given period from database

        :param start_date: date to fetch employees born after
        :param end_date: date to fetch employees born before
        :param strategy: loading strategy to be used for nested fields
        :return: employee born in given period
        """
        cls._check_strategy(strategy)

        employees = db.session.query(Employee).options(
            strategy(Employee.department)
        ).filter(
            and_(
                Employee.date_of_birth > start_date,
                Employee.date_of_birth < end_date
            )
        ).all()
        return employees
