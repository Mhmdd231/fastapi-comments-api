import re
import sqlite3
from pathlib import Path
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/comments"
DB_DIR = Path(__file__).resolve().parent.parent / "db"
DB_PATH = DB_DIR / "comments.db"

def count_words(text: str) -> int:
    return len(str(text).strip().split())

def clean_text(text: str) -> str:
    t = str(text).lower()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def chunk_text(text: str, chunk_size: int = 30):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i+chunk_size]
        if chunk_words:
            chunks.append(" ".join(chunk_words))
    return chunks

def ensure_database():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id INTEGER NOT NULL,
                chunk_text TEXT NOT NULL
            )
            """
        )

def insert_chunks(chunks):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "INSERT INTO comments (comment_id, chunk_text) VALUES (?, ?)",
            [(c["comment_id"], c["chunk_text"]) for c in chunks],
        )

def query_chunks_containing_python():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT chunk_text, comment_id
            FROM comments
            WHERE lower(chunk_text) LIKE '%python%'
            """
        ).fetchall()
    return [{"chunk_text": r[0], "comment_id": r[1]} for r in rows]

def main():
    print("Starting comment processing pipeline...")

    # Get comments from FastAPI
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    comments = data.get("comments", [])

    print(f"Total comments received: {len(comments)}")

    df = pd.DataFrame(comments)

    if df.empty:
        print("No comments returned from API.")
        return

    required_cols = {"id", "email", "body"}

    if not required_cols.issubset(set(df.columns)):
        raise ValueError("JSON missing required columns")

    # Count words
    df["body_word_count"] = (
        df["body"]
        .astype(str)
        .apply(count_words)
    )

    # Count .org emails
    org_count = (
        df["email"]
        .astype(str)
        .str.endswith(".org")
        .sum()
    )

    print(f".org emails found: {org_count}")

    # Filter comments
    filtered_df = df[
        df["email"].astype(str).str.endswith(".org")
        & (df["body_word_count"] > 20)
    ].copy()

    print(
        f"Comments passing filters: {len(filtered_df)}"
    )

    if filtered_df.empty:
        print("No rows matched filtering criteria.")
        return

    # Clean text
    filtered_df["clean_body"] = (
        filtered_df["body"]
        .astype(str)
        .apply(clean_text)
    )

    all_chunks = []

    for _, row in filtered_df.iterrows():

        comment_id = int(row["id"])

        chunks = chunk_text(
            row["clean_body"],
            chunk_size=30
        )

        for ch in chunks:
            all_chunks.append(
                {
                    "comment_id": comment_id,
                    "chunk_text": ch
                }
            )

    if not all_chunks:
        print("No chunks produced.")
        return

    print(f"Chunks created: {len(all_chunks)}")

    # Save to SQLite
    ensure_database()
    insert_chunks(all_chunks)

    print(f"Inserted data into: {DB_PATH}")

    # Search example
    results = query_chunks_containing_python()

    print(
        f"Chunks containing 'python': {len(results)}"
    )

    for item in results:
        print(
            f"- Comment ID: {item['comment_id']} | "
            f"Chunk: {item['chunk_text']}"
        )
if __name__ == "__main__":
    main()