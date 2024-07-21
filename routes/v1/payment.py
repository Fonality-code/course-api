from fastapi import APIRouter, HTTPException
from pydantic import ValidationError as PydanticValidationError
from typing import List
from beanie import PydanticObjectId
from datetime import datetime


router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)


# models

from models.payment import Payment, CreatePayment, PaymentStatus
from models.courses import Course

@router.post("/")
async def create_payment(payment: CreatePayment):

    # course exist
    course = await Course.get(payment.course_id)

    if not course:
        raise HTTPException(status_code=404, detail="course dose not exist")
    try:
        payment_doc = Payment(**payment.model_dump(), status=PaymentStatus.PENDING)
        await payment_doc.insert()
        return payment_doc
    except PydanticValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/")
async def get_payments():
    try:
        payments = await Payment.find_all().to_list()
        return payments
    except Exception as e:
        raise HTTPException(status_code=404, detail="erorr retriving payments")
    
@router.get("/{id}")
async def get_payment(id: PydanticObjectId):
    payment = await Payment.get(id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


