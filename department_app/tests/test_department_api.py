# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

import http
import json
from unittest.mock import patch

from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from department_app.rest.department_api import DepartmentApi
from department_app.tests.test_case_base import TestCaseBase
from department_app.tests.data import department_to_json, department_1, \
    department_2


class TestDepartmentApi(TestCaseBase):
    # pylint: disable=no-self-use

    def setUp(self) -> None:
        super().setUp()
        self.value_error = ValueError('Test Value Error Message')
        self.validation_error = ValidationError('Test Validation Error Message')
        self.failure_uuid = 'failure_uuid'

    def test_get_departments(self):
        mock_return_value = [department_1, department_2]

        with patch(
                'rest.department_api.DepartmentService.get_departments',
                autospec=True,
                return_value=mock_return_value
        ) as get_departments_mock:
            response = self.client.get('/api/departments')
            expected_json = [department_to_json(d) for d in mock_return_value]

            get_departments_mock.assert_called_once_with(strategy=selectinload)
            self.assertEqual(response.status_code, http.HTTPStatus.OK)
            self.assertEqual(response.json, expected_json)

    def test_get_department_success(self):
        mock_return_value = department_1

        with patch(
                'rest.department_api.DepartmentService.get_department_by_uuid',
                autospec=True,
                return_value=mock_return_value
        ) as get_department_by_uuid_mock:
            self.__test_get_department(
                get_department_by_uuid_mock,
                mock_return_value.uuid,
                http.HTTPStatus.OK,
                department_to_json(mock_return_value)
            )

    def test_get_department_failure(self):
        with patch(
                'rest.department_api.DepartmentService.get_department_by_uuid',
                side_effect=self.value_error
        ) as get_department_by_uuid_mock:
            self.__test_get_department(
                get_department_by_uuid_mock,
                self.failure_uuid,
                http.HTTPStatus.NOT_FOUND,
                DepartmentApi.NOT_FOUND_MESSAGE
            )

    def test_post_department_success(self):
        mock_return_value = department_2
        data = department_to_json(mock_return_value)

        with patch(
                'rest.department_api.DepartmentService.add_department',
                autospec=True,
                return_value=mock_return_value
        ) as add_department_success_mock:
            self.__test_post_department(
                data,
                add_department_success_mock,
                http.HTTPStatus.CREATED,
                data
            )

    def test_post_department_failure(self):
        data = department_to_json(department_2)

        with patch(
                'rest.department_api.DepartmentService.add_department',
                side_effect=self.validation_error
        ) as add_department_failure_mock:
            self.__test_post_department(
                data,
                add_department_failure_mock,
                http.HTTPStatus.BAD_REQUEST,
                self.validation_error.messages
            )

    def test_put_department_success(self):
        mock_return_value = department_2
        data = department_to_json(mock_return_value)

        with patch(
                'rest.department_api.DepartmentService.update_department',
                autospec=True,
                return_value=mock_return_value
        ) as update_department_success_mock:
            self.__test_put_department(
                data,
                update_department_success_mock,
                mock_return_value.uuid,
                http.HTTPStatus.OK,
                data
            )

    def test_put_department_failure(self):
        data = department_to_json(department_2)

        with patch(
                'rest.department_api.DepartmentService.update_department',
                side_effect=self.validation_error
        ) as update_department_failure_mock:
            self.__test_put_department(
                data,
                update_department_failure_mock,
                self.failure_uuid,
                http.HTTPStatus.BAD_REQUEST,
                self.validation_error.messages
            )

        with patch(
                'rest.department_api.DepartmentService.update_department',
                side_effect=self.value_error
        ) as add_department_failure_mock:
            self.__test_put_department(
                data,
                add_department_failure_mock,
                data['uuid'],
                http.HTTPStatus.NOT_FOUND,
                DepartmentApi.NOT_FOUND_MESSAGE
            )

    def test_delete_department_success(self):
        uuid = department_1.uuid

        with patch(
                'rest.department_api.DepartmentService.delete_department'
        ) as delete_department_success_mock:
            self.__test_delete_department(
                delete_department_success_mock,
                uuid,
                http.HTTPStatus.NO_CONTENT,
                DepartmentApi.NO_CONTENT_MESSAGE
            )

    def test_delete_department_failure(self):
        with patch(
                'rest.department_api.DepartmentService.delete_department',
                side_effect=self.value_error
        ) as delete_department_failure_mock:
            self.__test_delete_department(
                delete_department_failure_mock,
                self.failure_uuid,
                http.HTTPStatus.NOT_FOUND,
                DepartmentApi.NOT_FOUND_MESSAGE
            )

    def __test_get_department(self, get_department_by_uuid_mock, uuid,
                              expected_code, expected_json):
        response = self.client.get(f'/api/department/{uuid}')

        get_department_by_uuid_mock.assert_called_once_with(uuid)
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_post_department(self, data, add_department_mock,
                               expected_code, expected_json):
        response = self.client.post(
            '/api/departments',
            data=json.dumps(data),
            content_type='application/json'
        )
        # assert that 'add_department' was called once with data
        add_department_mock.assert_called_once()
        # pylint: disable=unused-variable
        name, args, kwargs = add_department_mock.mock_calls[0]
        self.assertEqual(args[1], data)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_put_department(self, data, update_department_mock, uuid,
                              expected_code, expected_json):
        response = self.client.put(
            f'/api/department/{uuid}',
            data=json.dumps(data),
            content_type='application/json',
        )
        # assert that 'update_department' was called once with uuid and data
        update_department_mock.assert_called_once()
        # pylint: disable=unused-variable
        name, args, kwargs = update_department_mock.mock_calls[0]
        self.assertEqual(args[1], uuid)
        self.assertEqual(args[2], data)

        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(response.json, expected_json)

    def __test_delete_department(self, delete_department_mock, uuid,
                                 expected_code, expected_str):
        response = self.client.delete(f'/api/department/{uuid}')

        delete_department_mock.assert_called_once_with(uuid)
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(
            response.get_data(as_text=True).strip('\n"'),
            expected_str
        )
