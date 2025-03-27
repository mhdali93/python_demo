# FastAPI Sample Application

This is a simple FastAPI application demonstrating basic GET and POST endpoints with advanced filtering and sorting capabilities.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Run the application using:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### Basic Endpoints
- `GET /`: Welcome message
- `GET /items/{item_id}`: Get a specific item by ID

### Advanced GET Endpoints

#### List Items with Filtering and Sorting
`GET /items` - List all items with optional filtering and sorting
Query Parameters:
- `name`: Filter by item name (case-insensitive partial match)
- `min_price`: Filter items with price greater than or equal to this value
- `max_price`: Filter items with price less than or equal to this value
- `sort_by`: Sort by field ("name" or "price")
- `order`: Sort order ("asc" or "desc")

Example:
```
GET /items?name=laptop&min_price=500&max_price=1000&sort_by=price&order=desc
```

#### Search Items
`GET /items/search/` - Advanced search endpoint
Query Parameters:
- `name`: Search in item names (case-insensitive partial match)
- `description`: Search in item descriptions (case-insensitive partial match)
- `min_price`: Filter by minimum price
- `max_price`: Filter by maximum price

Example:
```
GET /items/search/?name=laptop&description=gaming&min_price=500
```

### POST Endpoint
`POST /items` - Create a new item
- Validates that price is positive
- Validates that name is not empty
- Automatically assigns an ID

Example Request Body:
```json
{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop with RTX 3080",
    "price": 1999.99
}
```

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Example POST Request

```json
{
    "name": "Sample Item",
    "description": "This is a sample item",
    "price": 29.99
}
```