from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from utils import Utils

app = FastAPI(title="Sample FastAPI App")

# Sample data store (in-memory)
items = []

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Sample App"}

@app.get("/items", response_model=List[Item])
async def get_items(
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "name",
    order: SortOrder = SortOrder.ASC
):
    filtered_items = items.copy()
    
    # Filter by name if provided
    if name:
        filtered_items = [item for item in filtered_items if name.lower() in item.name.lower()]
    
    # Filter by price range if provided
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]
    
    # Sort items
    if sort_by == "name":
        filtered_items.sort(key=lambda x: x.name, reverse=(order == SortOrder.DESC))
    elif sort_by == "price":
        filtered_items.sort(key=lambda x: x.price, reverse=(order == SortOrder.DESC))
    
    return filtered_items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items/search/", response_model=List[Item])
async def search_items(
    name: Optional[str] = None,
    description: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    filtered_items = items.copy()
    
    if name:
        filtered_items = [item for item in filtered_items if name.lower() in item.name.lower()]
    if description:
        filtered_items = [item for item in filtered_items if description.lower() in (item.description or "").lower()]
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]
    
    return filtered_items

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    # Validate price is positive
    if item.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")
    
    # Validate name is not empty
    if not item.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # In a real application, you would use a database
    item.id = len(items) + 1
    items.append(item)
    Utils.heavy_print(items)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 