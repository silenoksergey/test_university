from pydantic import BaseModel, Field

from services.university.models.base_grade import GRADE_MIN, GRADE_MAX


class GradeStatResponse(BaseModel):
    count: int | None = Field(ge=0)
    min: int | None = Field(ge=GRADE_MIN, le=GRADE_MAX)
    max: int | None = Field(ge=GRADE_MIN, le=GRADE_MAX)
    avg: float | None = Field(ge=GRADE_MIN, le=GRADE_MAX)
