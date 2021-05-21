from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError

from department_app.models.employee import Employee
from department_app.service.department_service import DepartmentService


class DepartmentNested(fields.Nested):
    def __init__(self):
        super().__init__(
            'DepartmentSchema', exclude=('employees',), required=True
        )

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        try:
            department_uuid = data['department']['uuid']
            return DepartmentService.get_department_by_uuid(department_uuid)
        except KeyError:
            raise ValidationError('Department missing required field uuid')


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        exclude = ['id', 'department_id']
        load_instance = True
        include_fk = True

    department = DepartmentNested()
