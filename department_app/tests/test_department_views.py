import http
from department_app.tests.test_case_base import TestCaseBase


class TestHomepageViews(TestCaseBase):
    def test_departments(self):
        response = self.client.get('/departments')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_add_department(self):
        response = self.client.get('/department/add')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_edit_department(self):
        response = self.client.get('/department/edit')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response = self.client.get('/department/edit/some_uuid')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_delete_department(self):
        response = self.client.get('/department/delete')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response = self.client.get('/department/delete/some_uuid')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
