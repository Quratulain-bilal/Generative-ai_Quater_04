"""
COOKIE PARAMETERS DEMO
"Coffee Shop Punch Card"

Persistent client-side data.
Like loyalty punch cards.
"""

from typing import Optional
from fastapi import FastAPI, Cookie, Response

app = FastAPI()

@app.get("/visit")
async def track_visits(
    visits: int = Cookie(0, alias="customer_visits"),
    last_visit: Optional[str] = Cookie(None)
):
    """
    Example Cookies:
    customer_visits=3
    last_visit=2023-01-15
    
    Key Features:
    - Persistent across requests
    - Server can set cookies
    - Automatic type conversion
    - HttpOnly/Secure flags
    """
    
    from datetime import datetime
    response = Response(content=f"Visit #{visits + 1}")
    response.set_cookie(
        key="customer_visits",
        value=str(visits + 1),
        max_age=30*24*60*60  # 30 days
    )
    response.set_cookie(
        key="last_visit",
        value=datetime.now().isoformat()
    )
    return response