from services.general.base_service import BaseService
from services.university.helpers.grade_helper import GradesHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.teachers_helper import TeachersHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse
from services.university.models.grade_stat_request import GradeStatRequest
from services.university.models.grade_stat_response import GradeStatResponse
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.models.teachers_request import TeachersRequest
from services.university.models.teachers_response import TeachersResponse
from utils.api_utils import ApiUtils


class UniversityService(BaseService):
    SERVICE_URL = "http://localhost:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.grade_helper = GradesHelper(self.api_utils)
        self.teachers_helper = TeachersHelper(self.api_utils)

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponse(**response.json())

    def create_student(self, student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_students(json=student_request.model_dump())
        return StudentResponse(**response.json())

    def get_grades_stats(self, grade_stat_request: GradeStatRequest) -> GradeStatResponse:
        response = self.grade_helper.get_grades_stats(params=grade_stat_request.model_dump())
        return GradeStatResponse(**response.json())

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_create_grades(data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def create_teacher(self, teachers_request: TeachersRequest) -> TeachersResponse:
        response = self.teachers_helper.post_teachers(json=teachers_request.model_dump())
        return TeachersResponse(**response.json())
