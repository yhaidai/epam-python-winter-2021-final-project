# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

from unittest.mock import patch, MagicMock

from sqlalchemy.orm import selectinload

from department_app.service.department_service import DepartmentService
from department_app.schemas.department import DepartmentSchema
from department_app.tests.data import department_1, department_to_json
from department_app.tests.test_case_base import TestCaseBase


class TestDepartmentService(TestCaseBase):
    # pylint: disable=no-self-use

    def setUp(self) -> None:
        super().setUp()
        self.invalid_uuid = 'invalid_uuid'

    def test_get_departments(self):
        with patch(
                'service.department_service.StrategizedService._check_strategy'
        ) as check_strategy_mock, patch(
            'service.department_service.db.session',
            autospec=True
        ) as db_session_mock:
            strategy = selectinload
            DepartmentService.get_departments(strategy)
            db_session_mock.query().options.assert_called_once()
            check_strategy_mock.assert_called_once_with(strategy)

    def test_get_department_by_uuid_success(self):
        uuid = department_1.uuid
        with patch(
                'service.department_service.db.session', autospec=True
        ) as db_session_mock:
            DepartmentService.get_department_by_uuid(uuid)
            db_session_mock.query().filter_by.assert_called_once_with(
                uuid=uuid
            )

    def test_get_department_by_uuid_failure(self):
        with patch(
                'service.department_service.db.session', autospec=True
        ) as db_session_mock:
            db_session_mock.query().filter_by().first = MagicMock(
                return_value=None
            )

            with self.assertRaises(ValueError):
                DepartmentService.get_department_by_uuid(self.invalid_uuid)

            db_session_mock.query().filter_by.assert_called_with(
                uuid=self.invalid_uuid
            )

    def test_get_department_by_name_and_organisation(self):
        name = department_1.name
        organisation = department_1.organisation
        with patch(
                'service.department_service.db.session', autospec=True
        ) as db_session_mock:
            DepartmentService.get_department_by_name_and_organisation(
                name, organisation
            )
            db_session_mock.query().filter_by.assert_called_once_with(
                name=name, organisation=organisation
            )

    def test_add_department(self):
        mock_return_value = department_1
        with patch(
                'service.department_service.db.session', autospec=True
        ) as db_session_mock:
            department_json = department_to_json(mock_return_value)
            schema = DepartmentSchema
            schema.load = MagicMock(return_value=mock_return_value)
            result = DepartmentService.add_department(
                schema, department_json
            )

            schema.load.assert_called_once_with(
                department_json, session=db_session_mock
            )
            db_session_mock.add.assert_called_once_with(mock_return_value)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(mock_return_value, result)

    def test_update_department_success(self):
        mock_return_value = department_1
        uuid = mock_return_value.uuid
        department_json = department_to_json(mock_return_value)
        with patch(
                'service.department_service.db.session', autospec=True
        ) as db_session_mock, GetDepartmentByUUIDMock(
            return_value=mock_return_value
        ):
            schema = DepartmentSchema
            schema.load = MagicMock(return_value=mock_return_value)
            result = DepartmentService.update_department(
                schema, uuid, department_json
            )

            DepartmentService.get_department_by_uuid.assert_called_once_with(
                uuid
            )
            schema.load.assert_called_once_with(
                department_json,
                session=db_session_mock,
                instance=mock_return_value
            )
            db_session_mock.add.assert_called_once_with(mock_return_value)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(mock_return_value, result)

    def test_update_department_failure(self):
        with patch(
                'service.department_service.db.session', autospec=True
        ), GetDepartmentByUUIDMock():
            with self.assertRaises(ValueError):
                DepartmentService.update_department(
                    None, self.invalid_uuid, None
                )

            DepartmentService.get_department_by_uuid.assert_called_once_with(
                self.invalid_uuid
            )

    def test_delete_department_success(self):
        mock_return_value = department_1
        uuid = mock_return_value.uuid
        with patch(
                'service.department_service.db.session', autospec=True
        ) as db_session_mock, GetDepartmentByUUIDMock(
            return_value=mock_return_value
        ):
            DepartmentService.delete_department(uuid)
            DepartmentService.get_department_by_uuid.assert_called_once_with(
                uuid
            )
            db_session_mock.delete.assert_called_once_with(mock_return_value)
            db_session_mock.commit.assert_called_once()

    def test_delete_department_failure(self):
        with patch(
                'service.department_service.db.session', autospec=True
        ), GetDepartmentByUUIDMock():
            with self.assertRaises(ValueError):
                DepartmentService.delete_department(self.invalid_uuid)

            DepartmentService.get_department_by_uuid.assert_called_once_with(
                self.invalid_uuid
            )


# somehow patch didn't work, hence implementing it manually
class GetDepartmentByUUIDMock:
    def __init__(self, return_value=None):
        self.return_value = return_value
        self.original = DepartmentService.get_department_by_uuid

    def __enter__(self):
        DepartmentService.get_department_by_uuid = MagicMock(
            return_value=self.return_value
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        DepartmentService.get_department_by_uuid = self.original
