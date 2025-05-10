"""
FORM PARAMETERS DEMO
"Passport Application Form"

Traditional web form submission.
Like filling paper forms field by field.
"""

from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/register")
async def register_user(
    username: str = Form(..., min_length=4),
    password: str = Form(..., min_length=8),
    email: str = Form(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
):
    """
    Example Form Data:
    username=alikhan
    password=secure123
    email=ali@example.com
    
    Key Features:
    - application/x-www-form-urlencoded
    - Field-by-field submission
    - HTML form compatible
    - Requires python-multipart
    """
    return {
        "username": username,
        "email": email,
        "status": "registered"
    }