from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested

from department_app.models.employee import Employee


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        exclude = ['id', 'department_id']
        load_instance = True
        include_fk = True

    department = Nested('DepartmentSchema', exclude=('employees',))
