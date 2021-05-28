"""
Employee schema used to serialize/deserialize departments, this module
defines the following classes:

- `DepartmentNested`, nested department field for employee schema
- `EmployeeSchema`, employee serialization/deserialization schema
"""
# pylint: disable=cyclic-import

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError

from department_app.models.employee import Employee
from department_app.service.department_service import DepartmentService


class DepartmentNested(fields.Nested):
    """
    Nested department field for employee schema
    """
    def __init__(self):
        super().__init__(
            'DepartmentSchema', exclude=('employees',), required=True
        )

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        """
        Deserialize nested department field

        :param value: the value to be deserialized
        :param attr: the attribute/key in `data` to be deserialized
        :param data: the raw input data passed to the `Schema.load`
        :param partial: the ``partial`` parameter passed to `Schema.load`
        :param kwargs: field-specific keyword arguments
        :raise ValidationError: in case of data missing field uuid
        :return: the deserialized department
        """
        try:
            department_uuid = data['department']['uuid']
            return DepartmentService.get_department_by_uuid(department_uuid)
        except KeyError as error:
            raise ValidationError(
                'Department missing required field uuid'
            ) from error


class EmployeeSchema(SQLAlchemyAutoSchema):
    """
   Employee serialization/deserialization schema
   """
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Employee schema metadata
        """
        #: model to automatically generate schema from
        model = Employee

        #: fields excluded from schema
        exclude = ['id', 'department_id']

        #: deserialize to model instance
        load_instance = True

        #: include foreign keys into schema
        include_fk = True

    #: department the employee works in
    department = DepartmentNested()
