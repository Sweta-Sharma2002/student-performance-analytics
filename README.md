# Student Performance Analyzer

An interactive dashboard that analyzes exam performance for a class of 240 students
across 3 sections and 5 subjects — computing grades, rankings, at-risk flags, and the
correlation between study hours/attendance and scores.

**Live demo:** (https://student-performance-analytics-d5va3p4sp6kzxp5oxasn5n.streamlit.app/)

## Features
- Upload your own CSV or explore the built-in 240-student sample dataset
- Auto-computed Total, Average, Grade, Overall Rank, and Section Rank
- At-risk student detection (average < 50 or attendance < 65%)
- Study-hours-vs-score and attendance-vs-score correlation analysis
- Section-wise and subject-wise comparison charts
- Filterable leaderboard + downloadable CSV report

## Tech stack
Python, Pandas, NumPy, Matplotlib, Streamlit

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy for free (takes ~5 minutes)
1. Push this folder to a new GitHub repository (public).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
3. Click **"New app"**, select the repo, set the main file to `app.py`, and click **Deploy**.
4. Copy the live `.streamlit.app` URL it gives you — that's your demo link for your resume/GitHub.

## Files
```
app.py            # Streamlit dashboard
analysis.py       # Core analysis logic (shared with the notebook)
generate_data.py  # Synthetic dataset generator (240 students)
data/students.csv # Sample dataset
requirements.txt  # Dependencies
Student_Performance_Analyzer.ipynb  # Original notebook version, updated to match
```
