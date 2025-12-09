#!/usr/bin/env python3
"""Merge NHANES datasets on SEQN using dictionary-selected variables."""
from __future__ import annotations

from functools import reduce
from pathlib import Path
from typing import Iterable, List, Sequence

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DICT_PATH = BASE_DIR / "data_dictionary.xlsx"


def read_dictionary() -> List[str]:
    df = pd.read_excel(DICT_PATH)
    variables = [v for v in df["variable"].dropna().tolist()]
    return variables


DATASETS: Sequence[tuple[str, Sequence[str]]] = (
    ("ALQ_J.xpt", ("ALQ111", "ALQ130")),
    ("BPQ_J.xpt", ("BPQ020",)),
    ("DEMO_J.xpt", ("DMDEDUC2", "INDFMPIR", "RIAGENDR", "RIDAGEYR", "SEQN")),
    ("DPQ_J.xpt", ("DPQ020",)),
    ("MCQ_J.xpt", ("MCQ010", "MCQ080")),
    ("SLQ_J.xpt", ("SLD012", "SLD013", "SLQ050", "SLQ120")),
    ("SMQ_J .xpt", ("SMQ020", "SMQ040")),
)


FILE_DESCRIPTIONS = {
    "ALQ_J.xpt": "Alcohol use",
    "BPQ_J.xpt": "Blood pressure questionnaire",
    "DEMO_J.xpt": "Demographics",
    "DPQ_J.xpt": "Depression questionnaire",
    "MCQ_J.xpt": "Medical conditions",
    "SLQ_J.xpt": "Sleep",
    "SMQ_J .xpt": "Smoking",
}


def validate_dictionary(variables: Iterable[str]) -> None:
    mapped = {"SEQN"}
    for _, cols in DATASETS:
        mapped.update(cols)
    missing = sorted(set(variables) - mapped)
    if missing:
        raise ValueError(
            "Variables listed in the dictionary but not mapped to datasets: "
            + ", ".join(missing)
        )


def load_dataset(filename: str, columns: Sequence[str]) -> pd.DataFrame:
    path = BASE_DIR / filename
    df = pd.read_sas(path, format="xport", encoding="utf-8")
    if "SEQN" not in df.columns:
        raise ValueError(f"SEQN not found in {filename}")
    # Convert SEQN to nullable integers for consistent merging
    df["SEQN"] = pd.to_numeric(df["SEQN"], errors="raise").astype("Int64")
    needed = [c for c in columns if c != "SEQN"]
    missing_cols = [c for c in needed if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns {missing_cols} missing from {filename}")
    ordered_columns = ["SEQN"] + needed
    return df[ordered_columns]


def merge_datasets(datasets: Sequence[tuple[str, Sequence[str]]]) -> pd.DataFrame:
    frames = []
    for filename, cols in datasets:
        frame = load_dataset(filename, cols)
        frames.append(frame)
    merged = reduce(lambda left, right: pd.merge(left, right, on="SEQN", how="inner"), frames)
    ordered_cols = ["SEQN"] + [c for c in merged.columns if c != "SEQN"]
    merged = merged[ordered_cols].sort_values("SEQN").reset_index(drop=True)
    return merged


def main() -> None:
    variables = read_dictionary()
    validate_dictionary(variables)
    merged = merge_datasets(DATASETS)
    output_path = BASE_DIR / "merged_sleep_dataset.csv"
    merged.to_csv(output_path, index=False)
    print(
        f"Merged {len(DATASETS)} files (" + ", ".join(FILE_DESCRIPTIONS.values()) + ")"
    )
    print(f"Output rows: {len(merged)}, columns: {len(merged.columns)}")
    print(f"Saved merged dataset to {output_path}")


if __name__ == "__main__":
    main()
