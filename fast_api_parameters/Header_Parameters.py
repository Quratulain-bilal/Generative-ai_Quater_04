"""
HEADER PARAMETERS DEMO
"VIP Access Card"

Background metadata in HTTP headers.
Like showing VIP card at entrance.
"""

from typing import Optional
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/secure")
async def secure_endpoint(
    authorization: str = Header(..., alias="Authorization"),
    user_agent: Optional[str] = Header(None),
    x_api_key: str = Header(..., regex=r'^key-\d{3}$')
):
    """
    Example Headers:
    Authorization: Bearer abc123
    X-API-Key: key-123
    
    Key Features:
    - Automatic header name conversion
    - Case-insensitive
    - Special headers like User-Agent
    - Custom validation
    """
    return {
        "auth_type": authorization.split()[0],
        "client": user_agent,
        "api_key_valid": True
    }