from department_app import app

from . import employees
from . import departments
from . import homepage


def init_views():
    """
    Register views

    :return: None
    """
    employees.EmployeesView.register(app)
    departments.DepartmentsView.register(app)
    homepage.HomepageView.register(app)
