"""
Department model used to represent departments, this module defines the
following classes:

- `Department`, department model
"""
# pylint: disable=cyclic-import

import uuid

from department_app import db


class Department(db.Model):
    """
    Model representing department

    :param str name: name of the department
    :param str organisation: organisation the department belongs to
    :param employees: employees working in the department
    :type employees: list[Employee] or None
    """
    # pylint: disable=too-few-public-methods

    #: Name of the database table storing departments
    __tablename__ = 'department'

    #: Database id of the department
    id = db.Column(db.Integer, primary_key=True)

    #: Name of the department
    name = db.Column(db.String(64))

    #: Organisation the department belongs to
    organisation = db.Column(db.String(64))

    #: UUID of the department
    uuid = db.Column(db.String(36), unique=True)

    #: Employees working in the department
    employees = db.relationship(
        'Employee',
        cascade="all,delete",
        backref=db.backref('department', lazy=True),
        lazy=True
    )

    def __init__(self, name, organisation, employees=None):
        #: Name of the department
        self.name = name

        #: Organisation the department belongs to
        self.organisation = organisation

        #: UUID of the department
        self.uuid = str(uuid.uuid4())

        if employees is None:
            employees = []
        #: Employees working in the department
        self.employees = employees

    def __repr__(self):
        """
        Returns string representation of department

        :return: string representation of department
        """
        return f'Department({self.name}, {self.organisation})'
