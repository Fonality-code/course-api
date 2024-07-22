from pydantic import BaseModel, ConfigDict
from beanie import Document, Indexed
from enum import Enum
from datetime import datetime
from typing import Annotated, Optional


class ContentType(Enum):
    VIDEO = "video"
    DOCUMENT = "document"
    QUIZ = "quiz"
    YOUTUBE = "youtube"


class Content(Document):
    title: str
    course_id: Annotated[str, Indexed()]
    type: str
    description: str
    path: str
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class CreateContent(BaseModel):
    title: str
    course_id: str
    type: ContentType
    description: str
    path: str

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "course_id": "5eb7cf5a86d9755df3a6c593",
                "type": "youtube",
                "description": "video lecture on the importance of programming protocol",
                "path": "https://www.youtube.com/watch?v=xvb5hGLoK0A&t=595s",
            }
        },
    )


class UpdateContent(BaseModel):
    type: Optional[ContentType] = None
    description: Optional[str]  = None
    path: Optional[str] = None

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "type": "youtube",
                "description": "video lecture on the importance of programming protocol",
                "path": "https://www.youtube.com/watch?v=xvb5hGLoK0A&t=595s",
            }
        },
    )
