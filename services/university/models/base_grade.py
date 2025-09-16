from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: Annotated[int, Field(ge=0, le=5)]
