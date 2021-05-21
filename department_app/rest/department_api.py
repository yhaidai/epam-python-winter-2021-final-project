import json

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.schemas.department import DepartmentSchema
from department_app.service.department_service import DepartmentService


class DepartmentApiBase(Resource):
    schema = DepartmentSchema()
    service = DepartmentService()


class DepartmentListApi(DepartmentApiBase):
    def get(self):
        departments = self.service.get_departments(strategy=selectinload)
        return self.schema.dump(departments, many=True), 200

    def post(self):
        try:
            department = self.service.add_department(self.schema, request.json)
        except ValidationError as e:
            return e.messages, 400
        return self.schema.dump(department), 201


class DepartmentApi(DepartmentApiBase):
    NOT_FOUND_MESSAGE = 'Department not found'
    NO_CONTENT_MESSAGE = ''

    def get(self, uuid: str):
        try:
            department = self.service.get_department_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.schema.dump(department), 200

    def put(self, uuid):
        try:
            department = self.service.update_department(
                self.schema, uuid, request.json
            )
        except ValidationError as e:
            return e.messages, 400
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.schema.dump(department), 200

    def delete(self, uuid):
        try:
            self.service.delete_department(uuid)
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.NO_CONTENT_MESSAGE, 204
