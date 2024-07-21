from pydantic import BaseModel, ConfigDict

class HTTPError(BaseModel):
    detail: str

class ValidationError(BaseModel):
    loc: list
    msg: str
    type: str

class ErrorResponse(BaseModel):
    status_code: int
    message: str
    errors: str

    model_config = ConfigDict(
        extra='ignore', 
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "status_code": 404,
                "message": "Course not found",
                "errors": "Course not found"
            }
        }
    )



