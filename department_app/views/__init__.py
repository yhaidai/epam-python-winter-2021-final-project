"""
This package contains modules defining department and employee services:

Modules:

- `department_view.py`: defines department views
- `employee_view.py`: defines employee views
- `homepage_view.py`: defines homepage views
"""

from department_app import app

from . import employee_view
from . import department_view
from . import homepage_view


def init_views():
    """
    Register views

    :return: None
    """
    employee_view.EmployeeView.register(app)
    department_view.DepartmentView.register(app)
    homepage_view.HomepageView.register(app)
