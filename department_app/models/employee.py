import uuid

from department_app import db


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer)
    uuid = db.Column(db.String(36), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, date_of_birth, salary):
        self.name = name
        self.date_of_birth = date_of_birth
        self.salary = salary
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Employee({self.name}, {self.date_of_birth}, {self.salary})'
