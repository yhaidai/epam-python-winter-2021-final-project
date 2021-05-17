from flask import render_template
from flask_classy import FlaskView, route


class DepartmentsView(FlaskView):
    route_base = '/'

    @route('/departments', endpoint='departments')
    def departments(self):
        return render_template('departments.html')

    @route('/department/add', endpoint='add_department')
    def add_department(self):
        return render_template('department.html', expand='add')

    @route('/department/edit', endpoint='edit_department')
    @route('/department/edit/<uuid>', endpoint='edit_department')
    def edit_department(self, uuid):
        return render_template('department.html', uuid=uuid, expand='edit')

    @route('/department/delete', endpoint='delete_department')
    @route('/department/delete/<uuid>', endpoint='delete_department')
    def delete_department(self, uuid):
        return render_template('department.html', uuid=uuid, expand='delete')
