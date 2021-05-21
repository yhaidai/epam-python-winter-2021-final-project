import uuid

from department_app import db


class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    organisation = db.Column(db.String(64))
    uuid = db.Column(db.String(36), unique=True)
    employees = db.relationship(
        'Employee',
        cascade="all,delete",
        backref=db.backref('department', lazy=True),
        lazy=True
    )

    def __init__(self, name, organisation, employees=None):
        self.name = name
        self.organisation = organisation
        self.uuid = str(uuid.uuid4())
        if employees is None:
            employees = []
        self.employees = employees

    def __repr__(self):
        return f'Department({self.name}, {self.organisation})'
