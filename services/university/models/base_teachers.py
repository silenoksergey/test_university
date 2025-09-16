from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class SubjectEnum(StrEnum):
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    HISTORY = "History"
    BIOLOGY = "Biology"
    GEOGRAPHY = "Geography"


class BaseTeachers(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    subject: str
