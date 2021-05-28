# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

from datetime import date
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import selectinload

from department_app.service.employee_service import EmployeeService
from department_app.schemas.employee import EmployeeSchema
from department_app.tests.data import employee_1, employee_to_json, \
    employee_2, employee_5
from department_app.tests.test_case_base import TestCaseBase


class TestEmployeeService(TestCaseBase):
    # pylint: disable=no-self-use

    def setUp(self) -> None:
        super().setUp()
        self.invalid_uuid = 'invalid_uuid'

    def test_get_employees(self):
        with patch(
                'service.employee_service.StrategizedService._check_strategy'
        ) as check_strategy_mock, patch(
            'service.employee_service.db.session',
            autospec=True
        ) as db_session_mock:
            strategy = selectinload
            EmployeeService.get_employees(strategy)
            db_session_mock.query().options.assert_called_once()
            check_strategy_mock.assert_called_once_with(strategy)

    def test_get_employee_by_uuid_success(self):
        uuid = employee_1.uuid
        with patch(
                'service.employee_service.db.session', autospec=True
        ) as db_session_mock:
            EmployeeService.get_employee_by_uuid(uuid)
            db_session_mock.query().filter_by.assert_called_once_with(
                uuid=uuid
            )

    def test_get_employee_by_uuid_failure(self):
        with patch(
                'service.employee_service.db.session', autospec=True
        ) as db_session_mock:
            db_session_mock.query().filter_by().first = MagicMock(
                return_value=None
            )

            with self.assertRaises(ValueError):
                EmployeeService.get_employee_by_uuid(self.invalid_uuid)

            db_session_mock.query().filter_by.assert_called_with(
                uuid=self.invalid_uuid
            )

    def test_add_employee(self):
        mock_return_value = employee_1
        with patch(
                'service.employee_service.db.session', autospec=True
        ) as db_session_mock:
            employee_json = employee_to_json(mock_return_value)
            schema = EmployeeSchema
            schema.load = MagicMock(return_value=mock_return_value)
            result = EmployeeService.add_employee(
                schema, employee_json
            )

            schema.load.assert_called_once_with(
                employee_json, session=db_session_mock
            )
            db_session_mock.add.assert_called_once_with(mock_return_value)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(mock_return_value, result)

    def test_update_employee_success(self):
        mock_return_value = employee_1
        uuid = mock_return_value.uuid
        employee_json = employee_to_json(mock_return_value)
        with patch(
                'service.employee_service.db.session', autospec=True
        ) as db_session_mock, GetEmployeeByUUIDMock(
            return_value=mock_return_value
        ):
            schema = EmployeeSchema
            schema.load = MagicMock(return_value=mock_return_value)
            result = EmployeeService.update_employee(
                schema, uuid, employee_json
            )

            EmployeeService.get_employee_by_uuid.assert_called_once_with(
                uuid
            )
            schema.load.assert_called_once_with(
                employee_json,
                session=db_session_mock,
                instance=mock_return_value
            )
            db_session_mock.add.assert_called_once_with(mock_return_value)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(mock_return_value, result)

    def test_update_employee_failure(self):
        with patch(
                'service.employee_service.db.session', autospec=True
        ), GetEmployeeByUUIDMock():
            with self.assertRaises(ValueError):
                EmployeeService.update_employee(
                    None, self.invalid_uuid, None
                )

            EmployeeService.get_employee_by_uuid.assert_called_once_with(
                self.invalid_uuid
            )

    def test_delete_employee_success(self):
        mock_return_value = employee_1
        uuid = mock_return_value.uuid
        with patch(
                'service.employee_service.db.session', autospec=True
        ) as db_session_mock, GetEmployeeByUUIDMock(
            return_value=mock_return_value
        ):
            EmployeeService.delete_employee(uuid)
            EmployeeService.get_employee_by_uuid.assert_called_once_with(
                uuid
            )
            db_session_mock.delete.assert_called_once_with(mock_return_value)
            db_session_mock.commit.assert_called_once()

    def test_delete_employee_failure(self):
        with patch(
                'service.employee_service.db.session', autospec=True
        ), GetEmployeeByUUIDMock():
            with self.assertRaises(ValueError):
                EmployeeService.delete_employee(self.invalid_uuid)

            EmployeeService.get_employee_by_uuid.assert_called_once_with(
                self.invalid_uuid
            )

    def test_get_employees_by_date_of_birth(self):
        expected = [employee_1, employee_2]
        search_date = employee_1.date_of_birth

        with patch(
                'service.employee_service.StrategizedService._check_strategy'
        ) as check_strategy_mock, patch(
            'service.employee_service.db.session',
            autospec=True
        ) as db_session_mock:
            db_session_mock.query().options().filter_by().all = MagicMock(
                return_value=expected
            )
            strategy = selectinload
            result = EmployeeService.get_employees_by_date_of_birth(
                search_date, strategy
            )

            check_strategy_mock.assert_called_once_with(strategy)
            db_session_mock.query().options().filter_by.assert_called_with(
                date_of_birth=search_date
            )
            self.assertEqual(expected, result)

    def test_get_employees_born_in_period(self):
        expected = [employee_1, employee_2, employee_5]
        start_date = date(1992, 10, 10)
        end_date = date(1999, 7, 12)

        with patch(
                'service.employee_service.StrategizedService._check_strategy'
        ) as check_strategy_mock, patch(
            'service.employee_service.db.session',
            autospec=True
        ) as db_session_mock:
            db_session_mock.query().options().filter().all = MagicMock(
                return_value=expected
            )
            strategy = selectinload
            result = EmployeeService.get_employees_born_in_period(
                start_date, end_date, strategy
            )

            check_strategy_mock.assert_called_once_with(strategy)
            db_session_mock.query().options().filter.assert_called()
            self.assertEqual(expected, result)


# somehow patch didn't work, hence implementing it manually
class GetEmployeeByUUIDMock:
    def __init__(self, return_value=None):
        self.return_value = return_value
        self.original = EmployeeService.get_employee_by_uuid

    def __enter__(self):
        EmployeeService.get_employee_by_uuid = MagicMock(
            return_value=self.return_value
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        EmployeeService.get_employee_by_uuid = self.original
