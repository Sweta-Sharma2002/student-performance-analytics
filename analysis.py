"""
analysis.py
-----------
Core analysis logic for the Student Performance Analyzer.
Shared by both the Streamlit app and the standalone notebook so the
two never drift out of sync.
"""

import pandas as pd
import numpy as np

SUBJECT_COLUMNS = ["Mathematics", "Science", "English", "Computer Science", "Social Studies"]


def load_data(path_or_buffer) -> pd.DataFrame:
    df = pd.read_csv(path_or_buffer)
    missing = [c for c in SUBJECT_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected subject columns: {missing}")
    return df


def grade(avg: float) -> str:
    if avg >= 90:
        return "A+"
    elif avg >= 75:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 40:
        return "C"
    else:
        return "F"


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Add Total, Average, Grade, Rank, Section Rank, and At-Risk flag."""
    df = df.copy()
    df["Total"] = df[SUBJECT_COLUMNS].sum(axis=1)
    df["Average"] = (df["Total"] / len(SUBJECT_COLUMNS)).round(2)
    df["Grade"] = df["Average"].apply(grade)
    df["OverallRank"] = df["Total"].rank(ascending=False, method="min").astype(int)
    df["SectionRank"] = (
        df.groupby("Section")["Total"].rank(ascending=False, method="min").astype(int)
    )
    df["AtRisk"] = (df["Average"] < 50) | (df["Attendance"] < 65)
    return df.sort_values("OverallRank")


def section_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Section")
        .agg(
            Students=("Name", "count"),
            AvgScore=("Average", "mean"),
            AvgAttendance=("Attendance", "mean"),
            AvgStudyHours=("StudyHours", "mean"),
            AtRiskCount=("AtRisk", "sum"),
        )
        .round(2)
        .reset_index()
    )


def subject_summary(df: pd.DataFrame) -> pd.DataFrame:
    means = df[SUBJECT_COLUMNS].mean().round(2)
    return means.reset_index().rename(columns={"index": "Subject", 0: "AverageScore"})


def study_hours_correlation(df: pd.DataFrame) -> float:
    return round(df["StudyHours"].corr(df["Average"]), 3)


def attendance_correlation(df: pd.DataFrame) -> float:
    return round(df["Attendance"].corr(df["Average"]), 3)


def grade_distribution(df: pd.DataFrame) -> pd.Series:
    order = ["A+", "A", "B", "C", "F"]
    return df["Grade"].value_counts().reindex(order).fillna(0).astype(int)
