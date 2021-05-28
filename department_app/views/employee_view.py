"""
Employee views used to manage employees on web application, this module
defines the following classes:

- `EmployeeView`, class that defines employee views
"""

from flask import render_template
from flask_classy import FlaskView, route


class EmployeeView(FlaskView):
    """
    Employee views used to manage employees on web application
    """
    # pylint: disable=no-self-use

    #: base url route for all employee routes
    route_base = '/'

    @route('/employees', endpoint='employees')
    def employees(self):
        """
        Returns rendered `employees.html` template for url route
        `/employees` and endpoint `employees`

        :return: rendered `employees.html` template
        """
        return render_template('employees.html')

    @route('/employee/add', endpoint='add_employee')
    def add_employee(self):
        """
        Returns rendered `employee.html` template for url route
        `/employee/add` and endpoint `add_employee`

        :return: rendered `employee.html` template
        """
        return render_template('employee.html', expand='add')

    @route('/employee/edit', endpoint='edit_employee')
    @route('/employee/edit/<uuid>', endpoint='edit_employee')
    def edit_employee(self, uuid=None):
        """
        Returns rendered `employee.html` template for url routes
        `/employee/edit`, `/employee/edit/<uuid>` and endpoint
        `edit_employee`

        :return: rendered `employee.html` template
        """
        return render_template('employee.html', uuid=uuid, expand='edit')

    @route('/employee/delete', endpoint='delete_employee')
    @route('/employee/delete/<uuid>', endpoint='delete_employee')
    def delete_employee(self, uuid=None):
        """
        Returns rendered `employee.html` template for url routes
        `/employee/delete`, `/employee/delete/<uuid>` and endpoint
        `delete_employee`

        :return: rendered `employee.html` template
        """
        return render_template('employee.html', uuid=uuid, expand='delete')
