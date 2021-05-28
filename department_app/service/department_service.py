"""
Department service used to make database queries, this module defines the
following classes:

- `DepartmentService`, department service
"""
# pylint: disable=cyclic-import

from sqlalchemy.orm import lazyload

from department_app import db
from department_app.models.department import Department
from department_app.service.strategized_service import StrategizedService


class DepartmentService(StrategizedService):
    """
    Department service used to make database queries
    """
    @classmethod
    def get_departments(cls, strategy=lazyload):
        """
        Fetches all of the departments from database using given strategy

        :param strategy: loading strategy to be used for nested fields
        :return: list of all departments
        """
        cls._check_strategy(strategy)

        return db.session.query(Department).options(
                strategy(Department.employees)
            ).all()

    @staticmethod
    def get_department_by_uuid(uuid):
        """
        Fetches the department with given UUID from database, raises
        ValueError if such department is not found

        :param uuid: UUID of the department to be fetched
        :raise ValueError: in case of department with given UUID being absent
        in the database
        :return: department with given UUID
        """
        department = db.session.query(Department).filter_by(uuid=uuid).first()
        if department is None:
            raise ValueError('Invalid department uuid')
        return department

    @staticmethod
    def get_department_by_name_and_organisation(name, organisation):
        """
        Fetches the department with given name and organisation  from database,
        raises ValueError if such department is not found

        :param name: name of the department to be fetched
        :param organisation: organisation of the department to be fetched
        :return: department with given name and organisation
        """
        return db.session.query(Department).filter_by(
            name=name, organisation=organisation
        ).first()

    @staticmethod
    def add_department(schema, department_json):
        """
        Deserializes department and adds it to the database

        :param schema: schema to be used to deserialize the department
        :param department_json: data to deserialize the department from
        :return: department that was added
        """
        department = schema.load(department_json, session=db.session)
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def update_department(cls, schema, uuid, department_json):
        """
        Deserializes department and updates department with given UUID using
        latter, raises ValueError if department with given UUID is not found

        :param schema: schema to be used to deserialize the department
        :param uuid: UUID of the department to be updated
        :param department_json: data to deserialize the department from
        :raise ValueError: in case of department with given UUID being absent
        in the database
        :return: department that was updated
        """
        department = cls.get_department_by_uuid(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        department = schema.load(
            department_json, session=db.session, instance=department
        )
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def delete_department(cls, uuid):
        """
        Deletes the department with given UUID from database, raises
        ValueError if such department is not found

        :param uuid: UUID of the department to be deleted
        :raise ValueError: in case of department with given UUID being absent
        in the database
        :return: None
        """
        department = cls.get_department_by_uuid(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        db.session.delete(department)
        db.session.commit()
