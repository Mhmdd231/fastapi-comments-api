# FastAPI Comments API

A simple REST API built with **FastAPI** that reads comments from a CSV file and returns them as JSON data.

This project demonstrates backend API development using Python, FastAPI, and data processing with Pandas.

---

## Features

- Retrieve all comments through an API endpoint
- Read and process CSV data
- Convert CSV records into JSON responses
- Validate required CSV columns
- Handle missing files and server errors
- Automatic API documentation with Swagger UI

---

## Technologies Used

- Python 3
- FastAPI
- Pandas
- Uvicorn
- REST API
- JSON
- CSV

---

## Project Structure

```
fastapi-comments-api/

├── main.py
├── process.py
├── comments.csv
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mhmdd231/fastapi-comments-api.git
```

### 2. Move into the project folder

```bash
cd fastapi-comments-api
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

Start the server:

```bash
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive documentation.

## Screenshots

### Swagger API Documentation

![Swagger Documentation](screenshots/swagger.png)

## Swagger UI

Open:

```
http://127.0.0.1:8000/docs
```

You can test the API directly from your browser.

## ReDoc

Open:

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Get Comments

### Request

```
GET /comments
```

### Response Example

```json
{
  "comments": [
    {
      "id": 1,
      "email": "example@email.com",
      "body": "Example comment"
    }
  ]
}
```

---

## CSV Format

The API expects:

```csv
id,email,body
1,test@example.com,Hello world
```

---

## Error Handling

The API handles:

- Missing CSV file
- Invalid CSV format
- Missing required columns
- Server reading errors

---

## Future Improvements

- Add database support (PostgreSQL/MySQL)
- Add authentication
- Add pagination
- Add CRUD operations
- Add Docker support

---

## Author

Mhmdd231

GitHub:
https://github.com/Mhmdd231
