# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

import http

from department_app.tests.test_case_base import TestCaseBase


class TestHomepageViews(TestCaseBase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
