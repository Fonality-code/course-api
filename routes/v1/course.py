from fastapi import APIRouter, HTTPException
from pydantic import ValidationError as PydanticValidationError
from typing import List
from beanie import PydanticObjectId
from datetime import datetime



from models.courses import (
    CreateCourse,
    Course,
    UpdateCourse
)


from models.content import Content

from models.errors import (
    ErrorResponse, 
    HTTPError
)


router = APIRouter(
    prefix='/course',
    tags=['course'],
)

# Retrieve all courses
@router.get("/", response_model=List[Course])
async def get_courses():
    try: 
        courses = await Course.find_all().to_list()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve a specific course by ID
@router.get("/{id}", response_model=Course, responses={404: {"model": ErrorResponse}})
async def get_course(id: PydanticObjectId):
    course = await Course.get(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# Update a specific course by ID
@router.put("/{id}", response_model=Course, responses={404: {"model": ErrorResponse}})
async def update_course(id: PydanticObjectId, course_update: UpdateCourse):
    course = await Course.get(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    
    
    update_data = course_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)


    course.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    await course.save()
    return course


# create course
@router.post("/", response_model=Course, responses={422: {"model": ErrorResponse}})
async def create_course(course: CreateCourse):
    try:
        course_doc = Course(**course.model_dump())
        await course_doc.insert()
        return course_doc
    except PydanticValidationError as e:
        raise HTTPException(status_code=422, detail="Validation error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Delete a specific course by ID
@router.delete("/{id}", response_model=Course, responses={404: {"model": ErrorResponse}})
async def delete_course(id: PydanticObjectId):
    course = await Course.get(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # delete all contents associated with the course
    contents = await Content.find({'course_id': str(course.id)}).to_list()
    for content in contents:
        await content.delete()

    contents = await Content.find({'course_id': str(course.id)}).to_list()

    if len(contents) > 0:
        raise HTTPException(status_code=500, detail="Failed to delete course contents")
    
    await course.delete()
    return {
        "message": "Course deleted successfully"
    }
    
