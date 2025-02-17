from pathlib import Path
from typing import Callable

import pandas as pd


def create_search_record(session_id: str, session: pd.DataFrame) -> str:
    query = session.iloc[0]["query_text"]
    serp = "\t".join(session["url"].astype(str))

    return f"{session_id}\t0\tQ\t{query}\t0\t{serp}"


def create_click_record(session_id: str, row: pd.Series) -> str:
    return f"{session_id}\t0\tC\t{row['url']}"


def click_target(row: pd.Series) -> bool:
    return row["is_click"]


def convert_df(
    path_from: Path, path_to: Path, target: Callable[[pd.Series], bool] = click_target
) -> None:
    df = pd.read_csv(path_from, sep="\t")

    with open(path_to, "w", encoding="utf-8") as f_out:
        for session_id, session in df.groupby("session_id"):

            f_out.write(create_search_record(session_id, session))
            f_out.write("\n")

            for _, row in session.iterrows():
                if not target(row):
                    continue

                f_out.write(create_click_record(session_id, row))
                f_out.write("\n")
