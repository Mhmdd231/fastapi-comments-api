from fastapi import FastAPI, HTTPException
from pathlib import Path

from app.services.csv_reader import read_comments


app = FastAPI(
    title="Comments API",
    description="API that serves comments from a CSV file"
)


CSV_PATH = Path(__file__).resolve().parent.parent / "data/comments.csv"


@app.get("/comments")
def get_comments():

    if not CSV_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="CSV file not found"
        )

    try:
        comments = read_comments(CSV_PATH)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "comments": comments
    }