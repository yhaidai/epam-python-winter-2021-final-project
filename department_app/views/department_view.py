"""
Department views used to manage departments on web application, this module
defines the following classes:

- `DepartmentView`, class that defines department views
"""

from flask import render_template
from flask_classy import FlaskView, route


class DepartmentView(FlaskView):
    """
    Department views used to manage departments on web application
    """
    # pylint: disable=no-self-use

    #: base url route for all department routes
    route_base = '/'

    @route('/departments', endpoint='departments')
    def departments(self):
        """
        Returns rendered `departments.html` template for url route
        `/departments` and endpoint `departments`

        :return: rendered `departments.html` template
        """
        return render_template('departments.html')

    @route('/department/add', endpoint='add_department')
    def add_department(self):
        """
        Returns rendered `department.html` template for url route
        `/department/add` and endpoint `add_department`

        :return: rendered `department.html` template
        """
        return render_template('department.html', expand='add')

    @route('/department/edit', endpoint='edit_department')
    @route('/department/edit/<uuid>', endpoint='edit_department')
    def edit_department(self, uuid=None):
        """
        Returns rendered `department.html` template for url routes
        `/department/edit`, `/department/edit/<uuid>` and endpoint
        `edit_department`

        :return: rendered `department.html` template
        """
        return render_template('department.html', uuid=uuid, expand='edit')

    @route('/department/delete', endpoint='delete_department')
    @route('/department/delete/<uuid>', endpoint='delete_department')
    def delete_department(self, uuid=None):
        """
        Returns rendered `department.html` template for url routes
        `/department/delete`, `/department/delete/<uuid>` and endpoint
        `delete_department`

        :return: rendered `department.html` template
        """
        return render_template('department.html', uuid=uuid, expand='delete')
