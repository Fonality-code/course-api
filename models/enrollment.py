from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Annotated, Optional


"""
    - ID
    - Course ID
    - Student ID
    - Enrollment Date
    - Progress
    - Completed
"""


class Enrollment(Document):
    course_id: Annotated[str, Indexed()]
    student_id:Annotated[str, Indexed()]
    enrollment_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    progress: int = 0
    completed: bool = False

    class Settings:
        collection = "enrollments"



class CreateEnrollment(BaseModel):
    course_id: str
    student_id: str

    model_config = ConfigDict(
        extra='ignore',
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "course_id": "5eb7cf5a86d9755df3a6c593",
                "student_id": "5eb7cf5a86d9755df3a6c593",
            }
        }
    )

