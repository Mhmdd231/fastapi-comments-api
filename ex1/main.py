from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd

app = FastAPI(title="Comments API", description="Serves comments from a CSV file as JSON.")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "comments.csv"


@app.get("/comments")
def get_comments():
    """
    Read comments.csv and return rows as JSON list.
    Expected columns: id, email, body
    """
    if not CSV_PATH.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found at {CSV_PATH}")

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read CSV: {e}")

    expected_cols = {"id", "email", "body"}
    if not expected_cols.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail="CSV missing required columns: id, email, body")

    records = df.to_dict(orient="records")
    return {"comments": records}