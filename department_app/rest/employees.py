from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.schemas.employee import EmployeeSchema
from department_app.service.employee import EmployeeService


def get_date_or_none(date_str, date_format='%Y-%m-%d'):
    try:
        return datetime.strptime(date_str, date_format)
    except (ValueError, TypeError):
        return None


class EmployeeResourceBase(Resource):
    schema = EmployeeSchema()
    service = EmployeeService()


class EmployeeSearchResource(EmployeeResourceBase):
    parser = reqparse.RequestParser()
    parser.add_argument('date')
    parser.add_argument('start_date')
    parser.add_argument('end_date')

    def get(self):
        args = self.parser.parse_args()
        date = get_date_or_none(args['date'])
        start_date = get_date_or_none(args['start_date'])
        end_date = get_date_or_none(args['end_date'])

        if date:
            employees = self.service.get_employees_by_date_of_birth(
                date, strategy=selectinload
            )
        elif start_date and end_date:
            employees = self.service.get_employees_born_in_period(
                start_date, end_date, strategy=selectinload
            )
        else:
            return 'Bad date', 400
        return self.schema.dump(employees, many=True), 200


class EmployeeListResource(EmployeeResourceBase):
    def get(self):
        employees = self.service.get_employees(strategy=selectinload)
        return self.schema.dump(employees, many=True), 200

    def post(self):
        try:
            department = self.service.add_employee(self.schema, request.json)
        except ValidationError as e:
            return e.messages, 400
        except ValueError:
            return 'Department not found', 404
        return self.schema.dump(department), 201


class EmployeeResource(EmployeeResourceBase):
    def get(self, uuid: str):
        employee = self.service.get_employee_by_uuid(uuid)
        if employee is None:
            return 'Employee not found', 404
        return self.schema.dump(employee), 200

    def put(self, uuid: str):
        try:
            employee = self.service.update_employee(
                self.schema, uuid, request.json
            )
        except ValidationError as e:
            return e.messages, 400
        except ValueError:
            return 'Department not found', 404
        return self.schema.dump(employee), 200

    def delete(self, uuid: str):
        try:
            self.service.delete_employee(uuid)
        except ValueError:
            return 'Department not found', 204
        return '', 204
