import random
import time

import pytest
import requests
from faker import Faker

from logger.logger import Logger
from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teachers import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_stat_request import GradeStatRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teachers_request import TeachersRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils

faker = Faker()


@pytest.fixture(scope="session", autouse=True)
def auth_service_readiness():
    timeout = 180
    start_time = time.time()
    last_error = None
    while time.time() < start_time + timeout:
        try:
            response = requests.get(AuthService.SERVICE_URL + "/docs", timeout=5)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as exc:
            last_error = exc
            time.sleep(1)
    else:
        raise RuntimeError(f"Auth service wasn't started during '{timeout}' seconds.") from last_error


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    username = faker.user_name()
    password = faker.password(length=30,
                              special_chars=True,
                              digits=True,
                              lower_case=True,
                              upper_case=True)
    auth_service.register_user(register_request=RegisterRequest(username=username,
                                                                password=password,
                                                                password_repeat=password,
                                                                email=faker.email()))
    login_response = auth_service.login_user(login_request=LoginRequest(username=username,
                                                                        password=password))
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(url=AuthService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def prepare_two_grades(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)

    Logger.info("### Step 1. Create group")
    group = GroupRequest(name=faker.name())
    group_response = university_service.create_group(group_request=group)

    Logger.info("### Step 2. Create student")
    student = StudentRequest(first_name=faker.first_name(),
                             last_name=faker.last_name(),
                             email=faker.email(),
                             degree=random.choice([option for option in DegreeEnum]),
                             phone=faker.numerify("+7##########"),
                             group_id=group_response.id)
    student_response = university_service.create_student(student_request=student)

    Logger.info("### Step 3. Create teacher")
    teacher = TeachersRequest(first_name=faker.first_name(),
                              last_name=faker.last_name(),
                              subject=random.choice([option for option in SubjectEnum]))
    teacher_response = university_service.create_teacher(teachers_request=teacher)

    grades = []
    for i in range(2):
        Logger.info(f"### Step 4. Create grades #{i + 1}")
        grade = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=faker.random_int(min=0, max=5))
        grade_response = university_service.create_grade(grade_request=grade)
        grades.append(grade_response)
    g1, g2 = grades

    Logger.info("### Step 5. Get Grades Stats")
    grade_stats = GradeStatRequest(student_id=student_response.id,
                                   teacher_id=teacher_response.id,
                                   group_id=group_response.id)
    grade_stats_response = university_service.get_grades_stats(grade_stat_request=grade_stats)

    return g1, g2, grade_stats_response
