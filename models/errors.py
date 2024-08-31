from pydantic import BaseModel, ConfigDict


class HTTPError(BaseModel):
    detail: str


class ValidationError(BaseModel):
    loc: list
    msg: str
    type: str


class ErrorResponse(BaseModel):
    error: str
    details: list[ValidationError] | None = None

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "error": "Validation Error",
                "details": [
                    {
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ],
            }
        },
    )
