import json

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.schemas.department import DepartmentSchema
from department_app.service.department import DepartmentService


class DepartmentResourceBase(Resource):
    schema = DepartmentSchema()
    service = DepartmentService()


class DepartmentListResource(DepartmentResourceBase):
    def get(self):
        departments = self.service.get_departments(strategy=selectinload)
        return self.schema.dump(departments, many=True), 200

    def post(self):
        print(request.json)
        print()
        try:
            department = self.service.add_department(self.schema, json.loads(json.dumps(request.json)))
        except ValidationError as e:
            return e.messages, 400
        return self.schema.dump(department), 201


class DepartmentResource(DepartmentResourceBase):
    def get(self, uuid: str):
        try:
            department = self.service.get_department_by_uuid(uuid)
        except ValueError:
            return 'Department not found', 404
        return self.schema.dump(department), 200

    def put(self, uuid):
        print(request.json)
        try:
            department = self.service.update_department(
                self.schema, uuid, request.json
            )
        except ValidationError as e:
            print(e.messages)
            return e.messages, 400
        except ValueError:
            return 'Department not found', 404
        return self.schema.dump(department), 200

    def delete(self, uuid):
        try:
            self.service.delete_department(uuid)
        except ValueError:
            return 'Department not found', 204
        return '', 204
