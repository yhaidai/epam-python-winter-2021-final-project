"""
Department schema used to serialize/deserialize departments, this module
defines the following classes:

- `DepartmentSchema`, department serialization/deserialization schema
"""

# pylint: disable=cyclic-import

from marshmallow import validates_schema, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from department_app.models.department import Department
from department_app.service.department_service import DepartmentService


class DepartmentSchema(SQLAlchemyAutoSchema):
    """
    Department serialization/deserialization schema
    """
    # pylint: disable=too-few-public-methods, no-self-use

    class Meta:
        """
        Department schema metadata
        """
        #: model to automatically generate schema from
        model = Department

        #: fields excluded from schema
        exclude = ['id']

        #: deserialize to model instance
        load_instance = True

        #: include foreign keys into schema
        include_fk = True

        #: fields to provide only on serialization
        dump_only = ('employees',)

    #: average salary of the department employees
    average_salary = fields.Method('calculate_average_salary')

    #: employees working in the department
    employees = fields.Nested(
        'EmployeeSchema', many=True, exclude=('department',)
    )

    def calculate_average_salary(self, department):
        """
        Returns average salary of the department employees

        :param Department department: department to calculate average salary for
        :return float: average salary of the department employees
        """
        try:
            return sum(map(lambda employee: employee.salary,
                           department.employees)) / len(department.employees)
        except ZeroDivisionError:
            return 0

    # pylint: disable=unused-argument
    @validates_schema
    def validate_name_and_organisation_uniqueness(self, data, **kwargs):
        """
        Validate that there are no departments with the same name and
        organisation

        :param data: department data
        :raise ValidationError: in case exists another department with such name
        and organisation
        :return: None
        """
        department = DepartmentService.get_department_by_name_and_organisation(
            name=data['name'], organisation=data['organisation']
        )
        if department is not None:
            raise ValidationError(
                'Department name and organisation must be unique'
            )
