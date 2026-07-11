import pandas as pd


def read_comments(file_path):
    df = pd.read_csv(file_path)

    required_columns = {"id", "email", "body"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "CSV missing required columns: id, email, body"
        )

    return df.to_dict(orient="records")