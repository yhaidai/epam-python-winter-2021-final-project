"""
This package contains modules defining department and employee REST APIs and
functions to initialize respective API endpoints:

Modules:

- `department_api.py`: defines model representing departments
- `employee_api.py`: defines model representing employees

Functions:

- `init_api`: register REST API endpoints
"""
# pylint: disable=cyclic-import

from department_app import api

from . import department_api
from . import employee_api


def init_api():
    """
    Register REST Api endpoints

    :return: None
    """
    api.add_resource(
        department_api.DepartmentListApi,
        '/api/departments',
        strict_slashes=False
    )
    api.add_resource(
        department_api.DepartmentApi,
        '/api/department/<uuid>',
        strict_slashes=False
    )

    api.add_resource(
        employee_api.EmployeeListApi,
        '/api/employees',
        strict_slashes=False
    )
    api.add_resource(
        employee_api.EmployeeApi,
        '/api/employee/<uuid>',
        strict_slashes=False
    )
    api.add_resource(
        employee_api.EmployeeSearchApi,
        '/api/employees/search',
        strict_slashes=False
    )
