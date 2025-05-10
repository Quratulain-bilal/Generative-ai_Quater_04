"""
REQUEST BODY DEMO
"Complete Job Application Package"

Complex data sent in request body.
Like submitting full job application at once.
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI()

class Address(BaseModel):
    street: str = Field(..., example="123 Main St")
    city: str = Field(..., example="Karachi")
    postal_code: str = Field(..., regex=r'^\d{5}$')

class JobApplication(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    education: List[str] = Field(..., min_items=1)
    address: Address
    cover_letter: Optional[str] = None

@app.post("/applications")
async def submit_application(app: JobApplication):
    """
    Example JSON Body:
    {
      "name": "Ali Khan",
      "email": "ali@example.com",
      "education": ["BS Computer Science"],
      "address": {
        "street": "123 Main St",
        "city": "Karachi",
        "postal_code": "12345"
      }
    }
    
    Key Features:
    - Structured data validation
    - Nested models
    - Automatic documentation
    - JSON parsing
    """
    return {
        "status": "received",
        "applicant": app.name,
        "contact": app.email
    }