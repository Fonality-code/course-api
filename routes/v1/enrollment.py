from fastapi import APIRouter, HTTPException
from pydantic import ValidationError as PydanticValidationError
from typing import List
from beanie import PydanticObjectId
from datetime import datetime


router = APIRouter(
    prefix="/enrollment",
    tags=["enrollment"],
)


# models

from models.enrollment import Enrollment, CreateEnrollment
from models.courses import Course


@router.post("/")
async def create_enrollment(enrollment: CreateEnrollment):

    course = await Course.get(enrollment.course_id)

    if not course:
        raise HTTPException(status_code=404, detail="course dose not exist")
    try:
        enrollment_doc = Enrollment(**enrollment.model_dump())
        await enrollment_doc.insert()
        return enrollment_doc
    except PydanticValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_enrollments():
    try:
        enrollments = await Enrollment.find_all().to_list()
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=404, detail="erorr retriving enrollments")


@router.get("/{id}")
async def get_enrollment(id: PydanticObjectId):
    enrollment = await Enrollment.get(id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@router.delete("/{id}")
async def delete_enrollment(id: PydanticObjectId):
    enrollment = await Enrollment.get(id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    await enrollment.delete()
    return {"message": "Enrollment deleted successfully"}


# get all enrollments for a specific course
@router.get("/course/{course_id}")
async def get_enrollments_for_course(course_id: PydanticObjectId):
    enrollments = await Enrollment.find({"course_id": str(course_id)}).to_list()
    return enrollments
