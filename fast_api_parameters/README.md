# 🚀 FastAPI Parameter Mastery with Pydantic Validation

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)


## 🌟 Introduction
This comprehensive guide demonstrates all FastAPI parameter types with:
- Real-world analogies for easy understanding
- Pydantic validation examples
- Practical code implementations
- HTTP examples and responses

## 📋 Parameter Types

### 1. 🏠 Path Parameters
**"Visiting a Friend's House"**  
Essential fixed identifiers in your URL

```python
@app.get("/friends/{friend_id}")
async def get_friend(
    friend_id: int = Path(..., gt=0, example=45)
):
    return {"friend_id": friend_id}
Key Features:
✅ Part of URL path
✅ Required by default
✅ Position matters

2. 🔍 Query Parameters
"Ordering Custom Pizza"
Optional filters and customizations

python
@app.get("/pizza")
async def order_pizza(
    size: str = Query("medium", enum=["small", "medium", "large"]),
    toppings: list[str] = Query(["cheese"])
):
    return {"size": size, "toppings": toppings}
Key Features:
✅ Appear after ? in URL
✅ Key-value pairs
✅ Optional by default

3. 📦 Request Body
"Job Application Package"
Complete data submission

python
class Application(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    skills: list[str]

@app.post("/applications")
async def submit_application(app: Application):
    return {"status": "received", "name": app.name}
Key Features:
✅ Sent in request body
✅ Typically JSON format
✅ Handles complex data

4. 🎫 Header Parameters
"VIP Access Card"
Background authentication

python
@app.get("/vip")
async def vip_area(
    token: str = Header(..., alias="X-VIP-Token")
):
    return {"access": "granted"}
Key Features:
✅ Sent in HTTP headers
✅ Silent authentication
✅ Custom header names

5. 🍪 Cookie Parameters
"Coffee Punch Card"
Persistent client-side storage

python
@app.get("/coffee")
async def coffee_visit(
    visits: int = Cookie(0)
):
    return {"visits": visits + 1}
Key Features:
✅ Stored by browser
✅ Automatic sending
✅ Session tracking

6. 📝 Form Parameters
"Passport Application"
Traditional web form submission

python
@app.post("/passport")
async def apply_passport(
    name: str = Form(...),
    dob: date = Form(...)
):
    return {"status": "received"}
Key Features:
✅ application/x-www-form-urlencoded
✅ Field-by-field submission
✅ HTML form compatible

7. 📁 File Parameters
"USB Document Submission"
File uploads handling

python
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    return {"filename": file.filename}
**Key Features:
✅ Binary file transfer
✅ Multiple files support
✅ Metadata handling

🚨 Quick Reference Cheat Sheet
Parameter	Location	Example	Best For
Path	URL path	/users/42	Resource identification
Query	After ?	?page=2&size=10	Filtering/Sorting
Request Body	HTTP Body	JSON payload	Complex data
Header	HTTP Headers	Authorization: Bearer	Authentication
Cookie	HTTP Cookies	session_id=abc123	Session tracking
Form	Form-encoded	name=Ali&age=25	Web forms
File	Multipart	File upload	Document submission
💻 Installation
bash
# Install required packages
pip install fastapi uvicorn pydantic python-multipart

# Run the application
uvicorn main:app --reload
🏗️ Project Structure
fastapi-demo/
├── main.py               # Main application file
├── models.py             # Pydantic models
├── requirements.txt      # Dependencies
└── README.md            # This documentation
🌐 Real-World Examples
Instagram-like API:

python
@app.get("/profile/{username}")
async def get_profile(
    username: str,
    limit: int = Query(10, gt=0),
    token: str = Header(...)
):
    return {"profile": username, "posts": []}
E-commerce Filters:

python
@app.get("/products")
async def get_products(
    category: str = Query(...),
    min_price: float = Query(None, gt=0),
    max_price: float = Query(None, gt=0)
):
    return {"filters": {"category": category}}
🤝 Contributing
Fork the repository

Create your feature branch

Commit your changes

Push to the branch

Open a Pull Request

📜 License
MIT
