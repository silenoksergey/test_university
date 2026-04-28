import pytest
import requests.status_codes
from faker import Faker
from requests import codes

from services.university.helpers.grade_helper import GradesHelper

faker = Faker()


class TestGradesContract:
    def test_get_grades_stat_anonym(self, university_api_utils_anonym):
        grades_helper = GradesHelper(api_utils=university_api_utils_anonym)
        response = grades_helper.get_grades_stats(params={
            "student_id": faker.random_int(1, 10000),
            "teacher_id": faker.random_int(1, 10000),
            "group_id": faker.random_int(1, 10000)
        })
        assert response.status_code == requests.status_codes.codes.unauthorized, \
            (f"Wrong status code. Actual: '{response.status_code}',"
             f" but expected: '{codes.unauthorized}'")

    @pytest.mark.parametrize("bad_value", ["abc", 1.23])
    @pytest.mark.parametrize("param_name", ["student_id", "teacher_id", "group_id"])
    def test_validation_type_error(self, university_api_utils_admin, param_name, bad_value):
        grades_helper = GradesHelper(api_utils=university_api_utils_admin)
        params = {param_name: bad_value}
        response = grades_helper.get_grades_stats(params=params)
        assert response.status_code == codes.unprocessable_entity, \
            (f"Wrong status code. Actual: '{response.status_code}',"
             f" but expected: '{codes.unprocessable_entity}'")

    def test_grades_stats_all_params_success(self, university_api_utils_admin):
        grades_helper = GradesHelper(api_utils=university_api_utils_admin)
        response = grades_helper.get_grades_stats(params={
            "student_id": faker.random_int(1, 10000),
            "teacher_id": faker.random_int(1, 10000),
            "group_id": faker.random_int(1, 10000)
        })
        assert response.status_code == 200, \
            (f"Wrong status code. Actual: '{response.status_code}',"
             f" but expected: '{200}'")
