from pydantic import ConfigDict, BaseModel


class GradeStatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    student_id: int | None
    teacher_id: int | None
    group_id: int | None
