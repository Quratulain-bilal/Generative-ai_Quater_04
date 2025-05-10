import chainlit as cl
from pydantic import BaseModel, EmailStr, Field, validator, ValidationError
from typing import Optional
from datetime import datetime

# Pydantic models
class Address(BaseModel):
    street: str = Field(..., min_length=3, description="Street name (min 3 chars)")
    city: str = Field(..., min_length=2, description="City name")
    zip_code: str = Field(..., pattern=r'^\d{5}$', description="5-digit ZIP code")

class UserInfo(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    address: Address

    @validator('name')
    def name_valid(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name should only contain letters")
        return v.title()

# Field-wise models for validation
class NameOnly(BaseModel):
    name: str

    @validator('name')
    def name_valid(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name should only contain letters")
        return v.title()

class EmailOnly(BaseModel):
    email: EmailStr

class AgeOnly(BaseModel):
    age: int = Field(..., ge=13, le=120)

class StreetOnly(BaseModel):
    street: str = Field(..., min_length=3)

class CityOnly(BaseModel):
    city: str = Field(..., min_length=2)

class ZipOnly(BaseModel):
    zip_code: str = Field(..., pattern=r'^\d{5}$')


# Question list
QUESTIONS = [
    {"field": "name", "prompt": "📝 What is your full name? (2-50 letters)"},
    {"field": "email", "prompt": "📧 Your email address:"},
    {"field": "age", "prompt": "🎂 Your age (13-120):"},
    {"field": "street", "prompt": "🏡 Street address (min 3 characters):"},
    {"field": "city", "prompt": "🏙️ City:"},
    {"field": "zip_code", "prompt": "📮 5-digit ZIP code:"}
]

# Start of chat
@cl.on_chat_start
async def start():
    await cl.Message(content="🤖 Assalamu Alaikum! Let's begin.").send()
    cl.user_session.set("data", {})
    cl.user_session.set("step", 0)
    await ask_question()

# Ask next question
async def ask_question(error=None):
    step = cl.user_session.get("step", 0)
    if step >= len(QUESTIONS):
        await complete_form()
        return

    question = QUESTIONS[step]
    prompt = question["prompt"]

    if error:
        prompt = f"❌ {error}\n\n{prompt}"

    await cl.Message(content=prompt).send()

# Handle answers
async def process_answer(answer: str):
    step = cl.user_session.get("step", 0)
    field = QUESTIONS[step]["field"]
    data = cl.user_session.get("data", {})
    address = data.get("address", {})

    try:
        processed = answer.strip()

        # Individual field validation
        if field == "name":
            validated = NameOnly(name=processed)
            processed = validated.name
            data[field] = processed

        elif field == "email":
            validated = EmailOnly(email=processed)
            data[field] = validated.email

        elif field == "age":
            validated = AgeOnly(age=int(processed))
            data[field] = validated.age

        elif field == "street":
            validated = StreetOnly(street=processed)
            address["street"] = validated.street
            data["address"] = address

        elif field == "city":
            validated = CityOnly(city=processed)
            address["city"] = validated.city
            data["address"] = address

        elif field == "zip_code":
            validated = ZipOnly(zip_code=processed)
            address["zip_code"] = validated.zip_code
            data["address"] = address

        # Save and go to next question
        cl.user_session.set("data", data)
        cl.user_session.set("step", step + 1)
        await ask_question()

    except ValidationError as e:
        msg = e.errors()[0]['msg']
        await ask_question(msg)

# Final check
async def complete_form():
    data = cl.user_session.get("data", {})
    try:
        user = UserInfo(**data)
        summary = f"""
✅ **Validation Successful!**

**👤 Name:** {user.name}  
**📧 Email:** {user.email}  
**🎂 Age:** {user.age}  
**🏠 Address:**  
- {user.address.street}  
- {user.address.city}, {user.address.zip_code}
"""
        await cl.Message(content=summary).send()
        await cl.Message(content="🔄 Do you want to start over? (yes/no)").send()
        cl.user_session.set("complete", True)
    except ValidationError as e:
        await cl.Message(content=f"❌ Final Validation failed: {e}").send()
        await start()

# Restart option
@cl.on_message
async def main(message: cl.Message):
    if cl.user_session.get("complete"):
        await handle_complete(message)
        return
    await process_answer(message.content)

async def handle_complete(message: cl.Message):
    if message.content.lower() == "yes":
        cl.user_session.clear()
        await start()
    else:
        await cl.Message(content="🤖 Shukriya! Allah Hafiz!").send()

