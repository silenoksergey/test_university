import pytest
from faker import Faker
from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils

faker = Faker()


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
