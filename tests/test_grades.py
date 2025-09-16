import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teachers import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_stat_request import GradeStatRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teachers_request import TeachersRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGrades:
    def _prepare_two_grades(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)

        Logger.info(f"### Step 1. Create group")
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        Logger.info(f"### Step 2. Create student")
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+7##########"),
                                 group_id=group_response.id)
        student_response = university_service.create_student(student_request=student)

        Logger.info(f"### Step 3. Create teacher")
        teacher = TeachersRequest(first_name=faker.first_name(),
                                  last_name=faker.last_name(),
                                  subject=random.choice([option for option in SubjectEnum]))
        teacher_response = university_service.create_teacher(teachers_request=teacher)

        Logger.info(f"### Step 4. Create grades #1")
        grade_1 = GradeRequest(teacher_id=teacher_response.id,
                               student_id=student_response.id,
                               grade=faker.random_int(min=0, max=5))
        grade_response_1 = university_service.create_grade(grade_request=grade_1)

        Logger.info(f"### Step 4. Create grades #2")
        grade_2 = GradeRequest(teacher_id=teacher_response.id,
                               student_id=student_response.id,
                               grade=faker.random_int(min=0, max=5))
        grade_response_2 = university_service.create_grade(grade_request=grade_2)

        Logger.info(f"### Step 5. Get Grades Stats")
        grade_stats = GradeStatRequest(student_id=student_response.id,
                                       teacher_id=teacher_response.id,
                                       group_id=group_response.id)
        grade_stats_response = university_service.get_grades_stats(grade_stat_request=grade_stats)

        return grade_response_1, grade_response_2, grade_stats_response

    def test_grades_stats_count_is_two(self, university_api_utils_admin):
        g1, g2, stats = self._prepare_two_grades(university_api_utils_admin)
        assert stats.count == 2, f"Wrong grades count. Expected '2', Actual: {stats.count}"

    def test_grades_stats_min_correct(self, university_api_utils_admin):
        g1, g2, stats = self._prepare_two_grades(university_api_utils_admin)
        expected = min(g1.grade, g2.grade)
        assert stats.min == expected, f"Wrong min grades. Expected: {expected}, Actual: {stats.min}"

    def test_grades_stats_max_correct(self, university_api_utils_admin):
        g1, g2, stats = self._prepare_two_grades(university_api_utils_admin)
        expected = max(g1.grade, g2.grade)
        assert stats.max == expected, f"Wrong max grades. Expected: {expected}, Actual: {stats.max}"

    def test_grades_stats_avg_correct(self, university_api_utils_admin):
        g1, g2, stats = self._prepare_two_grades(university_api_utils_admin)
        expected = (g1.grade + g2.grade) / 2
        assert stats.avg == expected, f"Wrong avg grades. Expected: {expected}, Actual: {stats.avg}"
