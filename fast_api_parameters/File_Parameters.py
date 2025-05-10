"""
FILE PARAMETERS DEMO
"USB Document Submission"

File upload handling.
Like submitting documents at office.
"""

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/upload")
async def upload_document(
    document: UploadFile = File(..., description="PDF or image file"),
    description: str = Form(...)
):
    """
    Example Multipart Form:
    --------------------------
    Content-Disposition: form-data; name="document"; filename="doc.pdf"
    Content-Type: application/pdf
    
    <FILE DATA>
    --------------------------
    Content-Disposition: form-data; name="description"
    
    My important document
    --------------------------
    
    Key Features:
    - Handles large files
    - Streaming support
    - Metadata with form fields
    - File type validation
    """
    
    # Validate file type
    allowed_types = [
        "application/pdf", 
        "image/jpeg",
        "image/png"
    ]
    if document.content_type not in allowed_types:
        return JSONResponse(
            {"error": "Invalid file type"},
            status_code=400
        )
    
    return {
        "filename": document.filename,
        "type": document.content_type,
        "description": description,
        "size": f"{document.size / 1024:.1f} KB"
    }