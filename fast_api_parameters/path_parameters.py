"""
PATH PARAMETERS DEMO
"Visiting a Friend's House"

Essential identifiers in the URL path itself.
Like specifying exact house number to visit.
"""

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/products/{product_id}")
async def get_product(
    product_id: int = Path(
        ...,  # Required
        title="Product ID",
        gt=0,  # Must be greater than 0
        example=101,  # Example value
        description="The unique identifier for the product"
    )
):
    """
    Example Request: GET /products/101
    
    Key Features:
    - Embedded in URL path
    - Required by default
    - Position matters in route
    - Strong type conversion
    """
    return {
        "product_id": product_id,
        "name": f"Product {product_id}",
        "stock": 15
    }

# Nested path example
@app.get("/categories/{category_id}/products/{product_id}")
async def nested_path(
    category_id: int,
    product_id: int = Path(..., gt=0)
):
    return {
        "category": category_id,
        "product": product_id,
        "path": f"/categories/{category_id}/products/{product_id}"
    }