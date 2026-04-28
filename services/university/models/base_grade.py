from pydantic import BaseModel, ConfigDict, Field

GRADE_MIN = 0
GRADE_MAX = 5


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int = Field(ge=GRADE_MIN, le=GRADE_MAX)
