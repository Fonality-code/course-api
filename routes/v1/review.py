from fastapi import APIRouter, HTTPException
from pydantic import ValidationError as PydanticValidationError
from typing import List
from beanie import PydanticObjectId
from datetime import datetime


router = APIRouter(
    prefix="/review",
    tags=["review"],
)


# models
from models.review import Review, CreateReview
from models.courses import Course


@router.post("/")
async def create_review(review: CreateReview):

    course = await Course.get(review.course_id)

    if not course:
        raise HTTPException(status_code=404, detail="course dose not exist")
    try:
        review_doc = Review(**review.model_dump())
        await review_doc.insert()
        return review_doc
    except PydanticValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/")
async def get_reviews():
    try:
        reviews = await Review.find_all().to_list()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=404, detail="erorr retriving reviews")

@router.get("/{id}")
async def get_review(id: PydanticObjectId):
    review = await Review.get(id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.delete("/{id}")
async def delete_review(id: PydanticObjectId):
    review = await Review.get(id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    await review.delete()
    return {"message": "Review deleted successfully"}

@router.put("/{id}")
async def update_review(id: PydanticObjectId, review_update: CreateReview):
    review = await Review.get(id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    
    
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    await review.save()
    return review