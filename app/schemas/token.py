"""
Token Pydantic schemas
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """
    Base token schema
    """
    access_token: str
    token_type: str = "bearer"


class TokenResponse(Token):
    """
    Complete token response with refresh token
    """
    refresh_token: str
    expires_in: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }
    )


class TokenPayload(BaseModel):
    """
    JWT token payload
    """
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None
