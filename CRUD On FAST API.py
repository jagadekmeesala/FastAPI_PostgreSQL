from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Sample initial data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]

# Pydantic model for the item data
class Item(BaseModel):
    name: str

# CRUD operations

# Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    new_id = len(items) + 1
    new_item = {"id": new_id, "name": item.name}
    items.append(new_item)
    return new_item

# Read all items
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items

# Read a single item by ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update an item by ID
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    for existing_item in items:
        if existing_item["id"] == item_id:
            existing_item["name"] = item.name
            return existing_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item by ID
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            deleted_item = items.pop(index)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")
