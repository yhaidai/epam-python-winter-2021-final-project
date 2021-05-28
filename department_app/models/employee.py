"""
Employee model used to represent employees, this module defines the
following classes:

- `Employee`, employee model
"""
# pylint: disable=cyclic-import

import uuid

from department_app import db


class Employee(db.Model):
    """
    Model representing employee

    :param str name: employee's name
    :param date date_of_birth: employee's date of birth
    :param int salary: employee's salary
    :param department: department employee works in
    :type department: Department or None
    """
    # pylint: disable=too-few-public-methods

    #: Name of the database table storing employees
    __tablename__ = 'employee'

    #: employee's database id
    id = db.Column(db.Integer, primary_key=True)

    #: employee's name
    name = db.Column(db.String(64), nullable=False)

    #: employee's date of birth
    date_of_birth = db.Column(db.Date, nullable=False)

    #: employee's salary
    salary = db.Column(db.Integer)

    #: employee's uuid
    uuid = db.Column(db.String(36), unique=True)

    #: database id of the department employee works in
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, date_of_birth, salary=0, department=None):
        #: employee's name
        self.name = name

        #: employee's date of birth
        self.date_of_birth = date_of_birth

        #: employee's salary
        self.salary = salary

        #: employee's uuid
        self.uuid = str(uuid.uuid4())

        #: department employee works in
        self.department = department

    def __repr__(self):
        """
        Returns string representation of employee

        :return: string representation of employee
        """
        return f'Employee({self.name}, {self.date_of_birth}, {self.salary})'
