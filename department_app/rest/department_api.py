"""
Departments REST API, this module defines the following classes:

- `DepartmentApiBase`, department API base class
- `DepartmentListApi`, department list API class
- `DepartmentApi`, department API class
"""
# pylint: disable=cyclic-import

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.schemas.department import DepartmentSchema
from department_app.service.department_service import DepartmentService


class DepartmentApiBase(Resource):
    """
    Department API base class
    """
    #: Marshmallow schema used for department serialization/deserialization
    schema = DepartmentSchema()

    #: department database service
    service = DepartmentService()


class DepartmentListApi(DepartmentApiBase):
    """
    Department list API class
    """
    def get(self):
        """
        GET request handler of department list API

        Fetches all departments via service and returns them in a JSON format
        with a status code 200(OK)

        Uses selectinload loading strategy to fetch nested fields to solve
        the N+1 problem.

        :return: a tuple of all departments JSON and a status code 200
        """
        departments = self.service.get_departments(strategy=selectinload)
        return self.schema.dump(departments, many=True), 200

    def post(self):
        """
        POST request handler of department list API

        Deserializes request data, uses service to add the department to the
        database and returns newly added department in a JSON format with a
        status code 201(Created), or returns error messages with a status code
        400(Bad Request) in case of validation error during deserialization

        :return: a tuple of newly added department JSON and status code 201 or a
        tuple of error messages and status code 400 in case of validation error
        """
        try:
            department = self.service.add_department(self.schema, request.json)
        except ValidationError as error:
            return error.messages, 400
        return self.schema.dump(department), 201


class DepartmentApi(DepartmentApiBase):
    """
    Department API class
    """
    #: message to be returned in case of department not being found
    NOT_FOUND_MESSAGE = 'Department not found'

    #: message to be returned in case of department being successfully deleted
    NO_CONTENT_MESSAGE = ''

    def get(self, uuid: str):
        """
        GET request handler of department API

        Fetches the department with given uuid via service and returns it in a
        JSON format with a status code 200(OK), or returns an error message
        with a status code 404(Not Found) in case of department with given
        uuid not being found

        :return: a tuple of the department with given uuid in JSON and a status
        code 200, or a tuple of an error message and a status code 404 in
        case of department with given uuid not being found
        """
        try:
            department = self.service.get_department_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.schema.dump(department), 200

    def put(self, uuid):
        """
        PUT request handler of department API

        Uses service to deserialize request data and find the department with
        given uuid and update it with deserialized instance, returns updated
        department in a JSON format with a status code 201(Created), or returns
        error messages with a status code 400(Bad Request) in case of
        validation error during deserialization, or returns an error message
        with a status code 404(Not Found) in case of department with given uuid
        not being found

        :return: a tuple of updated department JSON and status code 200, or a
        tuple of error messages and status code 400 in case of validation
        error, or a tuple of an error message and a status code 404 in case of
        department with given uuid not being found
        """
        try:
            department = self.service.update_department(
                self.schema, uuid, request.json
            )
        except ValidationError as error:
            return error.messages, 400
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.schema.dump(department), 200

    def delete(self, uuid):
        """
        DELETE request handler of department API

        Uses service to delete the department with given uuid, returns no
        content message with a status code 204(No Content), or returns an error
        message with a status code 404(Not Found) in case of department with
        given uuid not being found

        :return: a tuple no content message and status code 204, or a tuple of
        an error message and a status code 404 in case of department with given
        uuid not being found
        """
        try:
            self.service.delete_department(uuid)
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.NO_CONTENT_MESSAGE, 204
