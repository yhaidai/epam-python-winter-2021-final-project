import http

from department_app.tests.test_case_base import TestCaseBase


class TestHomepageViews(TestCaseBase):
    def test_employees(self):
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_add_employee(self):
        response = self.client.get('/employee/add')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_edit_employee(self):
        response = self.client.get('/employee/edit')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response = self.client.get('/employee/edit/some_uuid')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_delete_employee(self):
        response = self.client.get('/employee/delete')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response = self.client.get('/employee/delete/some_uuid')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
