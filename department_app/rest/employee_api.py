"""
Departments REST API, this module defines the following classes:

- `EmployeeApiBase`, employee API base class
- `EmployeeSearchApi`, employee search API class
- `EmployeeListApi`, employee list API class
- `EmployeeApi`, employee API class
"""
# pylint: disable=cyclic-import

from datetime import datetime

from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.schemas.employee import EmployeeSchema
from department_app.service.employee_service import EmployeeService


def get_date_or_none(date_str, date_format='%Y-%m-%d'):
    """
    Returns date represented by date string and date format or None if date
    string has wrong type/doesn't match the format specified

    :param date_str: date string to convert into date object
    :param date_format: format of the date string
    :return: date object constructed from date string using date format or
    None in case of being unable to construct date object
    """
    try:
        return datetime.strptime(date_str, date_format).date()
    except (ValueError, TypeError):
        return None


class EmployeeApiBase(Resource):
    """
    Employee API base class
    """
    schema = EmployeeSchema()
    service = EmployeeService()


class EmployeeSearchApi(EmployeeApiBase):
    """
    Employee search API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('date')
    parser.add_argument('start_date')
    parser.add_argument('end_date')

    BAD_DATE_MESSAGE = 'Bad date'

    def get(self):
        """
        GET request handler of employee API

        Fetches the employees born on given date via service and returns them
        in a JSON format with a status code 200(OK).
        Or fetches the employees born in given period and returns them in a
        JSON format wth a status code 200(OK) in case of the exact date being
        unspecified/invalid.
        Or returns an error message with a status code 400(Bad Request) in
        case of both the exact date and the period being unspecified/invalid.

        Uses selectinload loading strategy while fetching nested fields to
        solve the N+1 problem.

        :return: a tuple of the employees born on given date in JSON and a
        status code 200, or a tuple of an error message and a status code 404
        in case of the exact date being unspecified/invalid, or a tuple of an
        error message and a status code 400.
        """
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
            return self.BAD_DATE_MESSAGE, 400

        return self.schema.dump(employees, many=True), 200


class EmployeeListApi(EmployeeApiBase):
    """
    Employee search list API class
    """
    def get(self):
        """
        GET request handler of employee list API

        Fetches all employees via service and returns them in a JSON format
        with a status code 200(OK)

        :return: a tuple of all employees JSON and a status code 200
        """
        employees = self.service.get_employees(strategy=selectinload)
        return self.schema.dump(employees, many=True), 200

    def post(self):
        """
        POST request handler of employee list API

        Deserializes request data, uses service to add the employee to the
        database and returns newly added employee in a JSON format with a
        status code 201(Created), or returns error messages with a status code
        400(Bad Request) in case of validation error during deserialization

        :return: a tuple of newly added employee JSON and status code 201 or a
        tuple of error messages and status code 400 in case of validation error
        """
        try:
            employee = self.service.add_employee(self.schema, request.json)
        except ValidationError as error:
            return error.messages, 400
        return self.schema.dump(employee), 201


class EmployeeApi(EmployeeApiBase):
    """
    Employee API class
    """
    NOT_FOUND_MESSAGE = 'Employee not found'
    NO_CONTENT_MESSAGE = ''

    def get(self, uuid: str):
        """
        GET request handler of employee API

        Fetches the employee with given uuid via service and returns it in a
        JSON format with a status code 200(OK), or returns an error message
        with a status code 404(Not Found) in case of employee with given
        uuid not being found

        :return: a tuple of the employee with given uuid in JSON and a status
        code 200, or a tuple of an error message and a status code 404 in
        case of employee with given uuid not being found
        """
        try:
            employee = self.service.get_employee_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.schema.dump(employee), 200

    def put(self, uuid: str):
        """
        PUT request handler of employee API

        Uses service to deserialize request data and find the employee with
        given uuid and update it with deserialized instance, returns updated
        employee in a JSON format with a status code 201(Created), or returns
        error messages with a status code 400(Bad Request) in case of
        validation error during deserialization, or returns an error message
        with a status code 404(Not Found) in case of employee with given uuid
        not being found

        :return: a tuple of updated employee JSON and status code 200, or a
        tuple of error messages and status code 400 in case of validation
        error, or a tuple of an error message and a status code 404 in case of
        employee with given uuid not being found
        """
        try:
            employee = self.service.update_employee(
                self.schema, uuid, request.json
            )
        except ValidationError as error:
            return error.messages, 400
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.schema.dump(employee), 200

    def delete(self, uuid: str):
        """
        DELETE request handler of employee API

        Uses service to delete the employee with given uuid, returns no
        content message with a status code 204(No Content), or returns an error
        message with a status code 404(Not Found) in case of employee with
        given uuid not being found

        :return: a tuple no content message and status code 204, or a tuple of
        an error message and a status code 404 in case of employee with given
        uuid not being found
        """
        try:
            self.service.delete_employee(uuid)
        except ValueError:
            return self.NOT_FOUND_MESSAGE, 404
        return self.NO_CONTENT_MESSAGE, 204
