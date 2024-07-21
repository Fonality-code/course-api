from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Annotated, Optional


"""
    - ID
    - Course ID
    - Student ID
    - Rating
    - Comment
    - Created At
"""


class Review(Document):
    course_id: Annotated[str, Indexed()]
    student_id: Annotated[str, Indexed()]
    rating: int
    comment: str
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    class Settings:
        collection = "reviews"


class CreateReview(BaseModel):
    course_id: str
    student_id: str
    rating: int
    comment: str

    model_config = ConfigDict(
        extra='ignore',
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "course_id": "5eb7cf5a86d9755df3a6c593",
                "student_id": "5eb7cf5a86d9755df3a6c593",
                "rating": 5,
                "comment": "This course was amazing!"
            }
        }
    )