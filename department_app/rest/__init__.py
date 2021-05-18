from department_app import api

from . import departments
from . import employees


def init_api():
    """
    Register REST Api endpoints

    :return: None
    """
    api.add_resource(
        departments.DepartmentListResource,
        '/api/departments',
        strict_slashes=False
    )
    api.add_resource(
        departments.DepartmentResource,
        '/api/department/<uuid>',
        strict_slashes=False
    )

    api.add_resource(
        employees.EmployeeListResource,
        '/api/employees',
        strict_slashes=False
    )
    api.add_resource(
        employees.EmployeeResource,
        '/api/employee/<uuid>',
        strict_slashes=False
    )
    api.add_resource(
        employees.EmployeeSearchResource,
        '/api/employees/search',
        strict_slashes=False
    )
