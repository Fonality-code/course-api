from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Annotated, Optional


"""
    - ID
    - User ID
    - Course ID
    - Amount
    - Status
    - Payment Date
"""


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class Payment(Document):
    user_id: Annotated[str, Indexed()]
    course_id: Annotated[str, Indexed()]
    amount: float
    status: PaymentStatus
    payment_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    class Settings:
        collection = "payments"



class CreatePayment(BaseModel):
    user_id: str
    course_id: str
    amount: float

    model_config = ConfigDict(
        extra='ignore',
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "5eb7cf5a86d9755df3a6c593",
                "course_id": "5eb7cf5a86d9755df3a6c593",
                "amount": 199.99
            }
        }
    )