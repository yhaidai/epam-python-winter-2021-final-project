import http
import json
from datetime import date, datetime, timedelta
from random import Random
from unittest.mock import patch

from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from rest.employee_api import EmployeeApi, EmployeeSearchApi, get_date_or_none
from tests.test_case_base import TestCaseBase
from data import employee_to_json, employee_1, employee_2, employee_3, \
    employee_4, employee_5


class TestEmployeeApi(TestCaseBase):
    def setUp(self) -> None:
        super().setUp()
        self.VALUE_ERROR = ValueError('Test Value Error Message')
        self.VALIDATION_ERROR = ValidationError('Test Validation Error Message')
        self.INVALID_UUID = 'invalid_uuid'
        self.INVALID_DATE = 'invalid date'
        self.random = Random()

    def test_get_employees(self):
        mock_return_value = [
            employee_1, employee_2, employee_3, employee_4, employee_5
        ]

        with patch(
                'rest.employee_api.EmployeeService.get_employees',
                autospec=True,
                return_value=mock_return_value
        ) as get_employees_mock:
            response = self.client.get('/api/employees')
            expected_json = [employee_to_json(d) for d in mock_return_value]

            get_employees_mock.assert_called_once_with(strategy=selectinload)
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(expected_json, response.json)

    def test_get_employee_success(self):
        mock_return_value = employee_1

        with patch(
                'rest.employee_api.EmployeeService.get_employee_by_uuid',
                autospec=True,
                return_value=mock_return_value
        ) as get_employee_by_uuid_mock:
            self.__test_get_employee(
                get_employee_by_uuid_mock,
                mock_return_value.uuid,
                http.HTTPStatus.OK,
                employee_to_json(mock_return_value)
            )

    def test_get_employee_failure(self):
        with patch(
                'rest.employee_api.EmployeeService.get_employee_by_uuid',
                side_effect=self.VALUE_ERROR
        ) as get_employee_by_uuid_mock:
            self.__test_get_employee(
                get_employee_by_uuid_mock,
                self.INVALID_UUID,
                http.HTTPStatus.NOT_FOUND,
                EmployeeApi.NOT_FOUND_MESSAGE
            )

    def test_post_employee_success(self):
        mock_return_value = employee_2
        data = employee_to_json(mock_return_value)

        with patch(
                'rest.employee_api.EmployeeService.add_employee',
                autospec=True,
                return_value=mock_return_value
        ) as add_employee_success_mock:
            self.__test_post_employee(
                data,
                add_employee_success_mock,
                http.HTTPStatus.CREATED,
                data
            )

    def test_post_employee_failure(self):
        data = employee_to_json(employee_2)

        with patch(
                'rest.employee_api.EmployeeService.add_employee',
                side_effect=self.VALIDATION_ERROR
        ) as add_employee_failure_mock:
            self.__test_post_employee(
                data,
                add_employee_failure_mock,
                http.HTTPStatus.BAD_REQUEST,
                self.VALIDATION_ERROR.messages
            )

    def test_put_employee_success(self):
        mock_return_value = employee_2
        data = employee_to_json(mock_return_value)

        with patch(
                'rest.employee_api.EmployeeService.update_employee',
                autospec=True,
                return_value=mock_return_value
        ) as update_employee_success_mock:
            self.__test_put_employee(
                data,
                update_employee_success_mock,
                mock_return_value.uuid,
                http.HTTPStatus.OK,
                data
            )

    def test_put_employee_failure(self):
        data = employee_to_json(employee_2)

        with patch(
                'rest.employee_api.EmployeeService.update_employee',
                side_effect=self.VALIDATION_ERROR
        ) as update_employee_failure_mock:
            self.__test_put_employee(
                data,
                update_employee_failure_mock,
                self.INVALID_UUID,
                http.HTTPStatus.BAD_REQUEST,
                self.VALIDATION_ERROR.messages
            )

        with patch(
                'rest.employee_api.EmployeeService.update_employee',
                side_effect=self.VALUE_ERROR
        ) as add_employee_failure_mock:
            self.__test_put_employee(
                data,
                add_employee_failure_mock,
                data['uuid'],
                http.HTTPStatus.NOT_FOUND,
                EmployeeApi.NOT_FOUND_MESSAGE
            )

    def test_delete_employee_success(self):
        uuid = employee_1.uuid

        with patch(
                'rest.employee_api.EmployeeService.delete_employee'
        ) as delete_employee_success_mock:
            self.__test_delete_employee(
                delete_employee_success_mock,
                uuid,
                http.HTTPStatus.NO_CONTENT,
                EmployeeApi.NO_CONTENT_MESSAGE
            )

    def test_delete_employee_failure(self):
        with patch(
                'rest.employee_api.EmployeeService.delete_employee',
                side_effect=self.VALUE_ERROR
        ) as delete_employee_failure_mock:
            self.__test_delete_employee(
                delete_employee_failure_mock,
                self.INVALID_UUID,
                http.HTTPStatus.NOT_FOUND,
                EmployeeApi.NOT_FOUND_MESSAGE
            )

    def test_search_employees_by_date_success(self):
        mock_return_value = [employee_1, employee_2]
        date = str(employee_1.date_of_birth)

        with patch(
                'rest.employee_api.EmployeeService.get_employees_by_date_of_birth',
                autospec=True,
                return_value=mock_return_value
        ) as get_employees_by_date_of_birth_success_mock:
            self.__test_search_employee_by_date(
                get_employees_by_date_of_birth_success_mock,
                date,
                http.HTTPStatus.OK,
                [employee_to_json(employee) for employee in mock_return_value]
            )

    def test_search_employees_by_date_failure(self):
        with patch(
                'rest.employee_api.EmployeeService.get_employees_by_date_of_birth'
        ) as get_employees_by_date_of_birth_failure_mock:
            self.__test_search_employee_by_date(
                get_employees_by_date_of_birth_failure_mock,
                self.INVALID_DATE,
                http.HTTPStatus.BAD_REQUEST,
                EmployeeSearchApi.BAD_DATE_MESSAGE,
                assert_mock_called=False
            )

    def test_search_employees_born_in_period_success(self):
        mock_return_value = [employee_1, employee_2, employee_5]
        start_date = str(date(1992, 10, 10))
        end_date = str(date(1999, 7, 12))

        with patch(
                'rest.employee_api.EmployeeService.get_employees_born_in_period',
                autospec=True,
                return_value=mock_return_value
        ) as get_employees_by_date_of_birth_success_mock:
            self.__test_search_employee_born_in_period(
                get_employees_by_date_of_birth_success_mock,
                start_date,
                end_date,
                http.HTTPStatus.OK,
                [employee_to_json(employee) for employee in mock_return_value]
            )

    def test_search_employees_born_in_period_failure(self):
        with patch(
                'rest.employee_api.EmployeeService.get_employees_born_in_period',
                side_effect=self.VALUE_ERROR
        ) as get_employees_by_date_of_birth_failure_mock:
            self.__test_search_employee_born_in_period(
                get_employees_by_date_of_birth_failure_mock,
                self.INVALID_DATE,
                self.INVALID_DATE,
                http.HTTPStatus.BAD_REQUEST,
                EmployeeSearchApi.BAD_DATE_MESSAGE,
                assert_mock_called=False
            )

    def test_get_date_or_none(self):
        round_count = 1_000
        min_year = date.today().year - 150
        max_year = date.today().year
        max_month = 12
        max_day = 28
        separators = [' ', '-', '.', '_', ', ', '/']
        year_formats = ['%Y']
        month_formats = ['%b', '%B', '%m']
        day_formats = ['%d']

        for _ in range(round_count):
            year = self.random.randint(min_year, max_year)
            month = self.random.randint(1, max_month)
            day = self.random.randint(1, max_day)
            separator = self.random.choice(separators)
            year_format = self.random.choice(year_formats)
            month_format = self.random.choice(month_formats)
            day_format = self.random.choice(day_formats)

            date_as_list = [year_format, month_format, day_format]
            self.random.shuffle(date_as_list)
            date_format = separator.join(date_as_list)

            with self.subTest(year=year, month=month, day=day):
                expected = date(year, month, day)
                valid_date_str = expected.strftime(date_format)
                self.assertEqual(
                    expected,
                    get_date_or_none(valid_date_str, date_format)
                )

        date_str = '2000-05-20'
        date_formats = [
            '%Y-%d-%m', '%d-%m-%Y', '%y-%d-%m', '%Y-%d-%b', '%Y-%d-%B'
        ]
        for date_format in date_formats:
            self.assertIsNone(get_date_or_none(date_str, date_format))

    def __test_get_employee(
            self,
            get_employee_by_uuid_mock,
            uuid,
            expected_code,
            expected_json
    ):
        response = self.client.get(f'/api/employee/{uuid}')

        get_employee_by_uuid_mock.assert_called_once_with(uuid)
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_post_employee(self,
                             data,
                             add_employee_mock,
                             expected_code,
                             expected_json
                             ):
        response = self.client.post(
            '/api/employees',
            data=json.dumps(data),
            content_type='application/json'
        )
        # assert that 'add_employee' was called once with data
        add_employee_mock.assert_called_once()
        name, args, kwargs = add_employee_mock.mock_calls[0]
        self.assertEqual(args[1], data)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_put_employee(
            self,
            data,
            update_employee_mock,
            uuid,
            expected_code,
            expected_json
    ):
        response = self.client.put(
            f'/api/employee/{uuid}',
            data=json.dumps(data),
            content_type='application/json',
        )
        # assert that 'update_employee' was called once with uuid and data
        update_employee_mock.assert_called_once()
        name, args, kwargs = update_employee_mock.mock_calls[0]
        self.assertEqual(args[1], uuid)
        self.assertEqual(args[2], data)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_delete_employee(
            self,
            delete_employee_mock,
            uuid,
            expected_code,
            expected_str
    ):
        response = self.client.delete(f'/api/employee/{uuid}')

        delete_employee_mock.assert_called_once_with(uuid)
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(
            response.get_data(as_text=True).strip('\n"'),
            expected_str
        )

    def __test_search_employee_by_date(
            self,
            search_employees_mock,
            date,
            expected_code,
            expected_json,
            assert_mock_called=True
    ):
        response = self.client.get(f'/api/employees/search?date={date}')

        if assert_mock_called:
            search_employees_mock.assert_called_once_with(
                datetime.strptime(date, '%Y-%m-%d').date(),
                strategy=selectinload
            )
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_search_employee_born_in_period(
            self,
            search_employees_mock,
            start_date,
            end_date,
            expected_code,
            expected_json,
            assert_mock_called=True
    ):
        url = f'/api/employees/search?start_date={start_date}&end_date={end_date}'
        response = self.client.get(url)

        if assert_mock_called:
            search_employees_mock.assert_called_once_with(
                datetime.strptime(start_date, '%Y-%m-%d').date(),
                datetime.strptime(end_date, '%Y-%m-%d').date(),
                strategy=selectinload
            )
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)
