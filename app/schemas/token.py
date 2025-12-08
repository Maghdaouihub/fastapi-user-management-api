"""
Token Pydantic schemas for authentication
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Access token response"""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload data"""

    sub: Optional[int] = None
    exp: Optional[int] = None


class RefreshToken(BaseModel):
    """Refresh token request"""

    refresh_token: str


class TokenPair(BaseModel):
    """Access and refresh token pair"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
