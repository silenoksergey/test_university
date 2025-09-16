from typing import Annotated

from pydantic import BaseModel, Field


class GradeStatResponse(BaseModel):
    count: Annotated[int, Field(ge=0)]
    min: Annotated[int, Field(ge=0, le=5)] | None
    max: Annotated[int, Field(ge=0, le=5)] | None
    avg: Annotated[float, Field(ge=0, le=5)] | None
