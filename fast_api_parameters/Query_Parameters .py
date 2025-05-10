"""
QUERY PARAMETERS DEMO
"Pizza Customization Options"

Optional filters after ? in URL.
Like specifying pizza toppings and size.
"""

from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

@app.get("/products")
async def filter_products(
    category: str = Query(..., min_length=3),
    min_price: float = Query(None, gt=0),
    max_price: float = Query(None, gt=0),
    sizes: List[str] = Query(["M"], alias="size"),
    in_stock: bool = Query(True)
):
    """
    Example Request: 
    GET /products?category=electronics&min_price=100&size=S&size=L
    
    Key Features:
    - Appear after ? in URL
    - Multiple values allowed (lists)
    - Optional parameters
    - Default values
    - Aliases for JS-friendly names
    """
    return {
        "filters": {
            "category": category,
            "price_range": f"{min_price}-{max_price}",
            "sizes": sizes,
            "in_stock": in_stock
        }
    }