from marshmallow import validates_schema, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested

from department_app.models.department import Department
from department_app.service.department import DepartmentService


class DepartmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        exclude = ['id']
        load_instance = True
        include_fk = True

    average_salary = fields.Method('calculate_average_salary')
    employees = Nested(
        'EmployeeSchema', many=True, exclude=('department', 'department_id')
    )

    def calculate_average_salary(self, department):
        try:
            return sum(map(lambda employee: employee.salary,
                       department.employees)) / len(department.employees)
        except ZeroDivisionError:
            return 0

    @validates_schema
    def validate_name_and_organisation_uniqueness(self, data, **kwargs):
        department = DepartmentService.get_department_by_name_and_organisation(
            name=data['name'], organisation=data['organisation']
        )
        if department is not None:
            raise ValidationError(
                'Department name and organisation must be unique'
            )
