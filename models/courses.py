from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Annotated, Optional

class CourseType(str, Enum):
    PRE_RECORDED = "pre-recorded"
    LIVE_BOOT = "life-boot"
    


class Course(Document):
    title: str 
    description: str 
    category: str 
    thumbnail: str
    type: Annotated[str, Indexed]
    instructor_id: Annotated[str, Indexed]
    price: float
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    class Settings:
        collection = "courses"



class CreateCourse(BaseModel):
    title: str 
    description: str 
    category: str 
    type: CourseType
    instructor_id: str 
    price: float
    thumbnail: str
    
    
    model_config = ConfigDict(
        extra='ignore', 
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Advanced Python Programming",
                "description": "An in-depth course on advanced Python programming concepts.",
                "category": "Programming",
                "type": "pre-recorded",
                "instructor_id": "12345",
                "price": 299.99,
                "thumbnail": "https://www.example.com/image.png"
            }
        }
    )


class UpdateCourse(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    type: Optional[CourseType] = None
    instructor_id: Optional[str] = None
    price: Optional[float] = None