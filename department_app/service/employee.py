from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, \
    raiseload, noload

from department_app import db
from department_app.models.employee import Employee
from department_app.models.department import Department
from department_app.service.department import DepartmentService


class EmployeeService:
    strategies = {
        lazyload, joinedload, subqueryload, selectinload, raiseload, noload
    }

    @classmethod
    def get_employees(cls, strategy=lazyload):
        if strategy not in cls.strategies:
            raise ValueError(
                f'Unsupported strategy. Only {cls.strategies} are allowed')

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
    def update_employee(cls, schema, uuid, department_json):
        department = cls.get_employee_by_uuid(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        department = schema.load(
            department_json, session=db.session, instance=department
        )
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def delete_employee(cls, uuid):
        employee = cls.get_employee_by_uuid(uuid)
        if employee is None:
            raise ValueError('Invalid employee uuid')
        db.session.delete(employee)
        db.session.commit()
