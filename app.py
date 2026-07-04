"""
app.py
------
Student Performance Analyzer — interactive Streamlit dashboard.

Run locally:   streamlit run app.py
Deploy free:   push this repo to GitHub -> share.streamlit.io -> "New app"
"""

import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analysis import (
    load_data, enrich, section_summary, subject_summary,
    study_hours_correlation, attendance_correlation, grade_distribution,
    SUBJECT_COLUMNS,
)

st.set_page_config(page_title="Student Performance Analyzer", layout="wide", page_icon="📊")

st.title("📊 Student Performance Analyzer")
st.caption("Upload a class result sheet or explore the built-in sample dataset of 240 students.")

# ---------------- Sidebar: data source ----------------
st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload a CSV (same columns as sample)", type=["csv"])

if uploaded is not None:
    raw_df = load_data(uploaded)
    st.sidebar.success(f"Loaded {len(raw_df)} students from your file.")
else:
    raw_df = load_data("data/students.csv")
    st.sidebar.info(f"Using sample dataset ({len(raw_df)} students). Upload your own CSV to replace it.")

df = enrich(raw_df)

# ---------------- Sidebar: filters ----------------
st.sidebar.header("Filters")
sections = sorted(df["Section"].unique())
selected_sections = st.sidebar.multiselect("Section", sections, default=sections)
grade_filter = st.sidebar.multiselect("Grade", ["A+", "A", "B", "C", "F"], default=["A+", "A", "B", "C", "F"])
show_at_risk_only = st.sidebar.checkbox("Show at-risk students only", value=False)

filtered = df[df["Section"].isin(selected_sections) & df["Grade"].isin(grade_filter)]
if show_at_risk_only:
    filtered = filtered[filtered["AtRisk"]]

# ---------------- KPI row ----------------
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Students", len(filtered))
col2.metric("Class Average", f"{filtered['Average'].mean():.1f}" if len(filtered) else "—")
col3.metric("Top Score", f"{filtered['Average'].max():.1f}" if len(filtered) else "—")
col4.metric("At-Risk Students", int(filtered["AtRisk"].sum()))
col5.metric("Avg. Attendance", f"{filtered['Attendance'].mean():.1f}%" if len(filtered) else "—")

st.divider()

# ---------------- Charts ----------------
left, right = st.columns(2)

with left:
    st.subheader("Grade Distribution")
    dist = grade_distribution(filtered)
    fig, ax = plt.subplots()
    ax.bar(dist.index, dist.values, color="#4C78A8")
    ax.set_ylabel("Number of Students")
    st.pyplot(fig)

with right:
    st.subheader("Study Hours vs. Average Score")
    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered["StudyHours"], filtered["Average"], alpha=0.5, color="#F58518")
    ax2.set_xlabel("Study Hours / Day")
    ax2.set_ylabel("Average Score")
    corr = study_hours_correlation(filtered) if len(filtered) > 1 else float("nan")
    ax2.set_title(f"Correlation: {corr}")
    st.pyplot(fig2)

st.subheader("Subject-wise Average Scores")
subj = filtered[SUBJECT_COLUMNS].mean().sort_values(ascending=False)
fig3, ax3 = plt.subplots()
ax3.barh(subj.index, subj.values, color="#54A24B")
ax3.set_xlabel("Average Score")
st.pyplot(fig3)

st.subheader("Section Comparison")
st.dataframe(section_summary(filtered), use_container_width=True)

st.divider()

# ---------------- Leaderboard & data table ----------------
tab1, tab2, tab3 = st.tabs(["🏆 Top 10", "⚠️ At-Risk List", "📋 Full Data"])

with tab1:
    st.dataframe(
        filtered.nsmallest(10, "OverallRank")[
            ["OverallRank", "Name", "Section", "Total", "Average", "Grade"]
        ],
        use_container_width=True, hide_index=True,
    )

with tab2:
    at_risk = filtered[filtered["AtRisk"]][
        ["Name", "Section", "Average", "Attendance", "Grade"]
    ]
    if at_risk.empty:
        st.success("No at-risk students in the current filter.")
    else:
        st.dataframe(at_risk, use_container_width=True, hide_index=True)

with tab3:
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# ---------------- Download ----------------
csv_buffer = io.StringIO()
filtered.to_csv(csv_buffer, index=False)
st.download_button(
    "⬇️ Download filtered report as CSV",
    data=csv_buffer.getvalue(),
    file_name="student_performance_report.csv",
    mime="text/csv",
)

st.caption("Built with Python, Pandas & Streamlit — by Sweta Sharma")
