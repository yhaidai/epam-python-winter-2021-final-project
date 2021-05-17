from flask import render_template
from flask_classy import FlaskView, route


class EmployeesView(FlaskView):
    route_base = '/'

    @route('/employees', endpoint='employees')
    def employees(self):
        return render_template('employees.html')

    @route('/employee/add', endpoint='add_employee')
    def add_employee(self):
        return render_template('employee.html', expand='add')

    @route('/employee/edit', endpoint='edit_employee')
    @route('/employee/edit/<uuid>', endpoint='edit_employee')
    def edit_employee(self, uuid):
        return render_template('employee.html', uuid=uuid, expand='edit')

    @route('/employee/delete', endpoint='delete_employee')
    @route('/employee/delete/<uuid>', endpoint='delete_employee')
    def delete_employee(self, uuid):
        return render_template('employee.html', uuid=uuid, expand='delete')
