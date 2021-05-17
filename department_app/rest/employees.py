from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.schemas.employee import EmployeeSchema
from department_app.service.employee import EmployeeService


class EmployeeListResource(Resource):
    schema = EmployeeSchema()
    service = EmployeeService()

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


class EmployeeResource(Resource):
    schema = EmployeeSchema()
    service = EmployeeService()

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
