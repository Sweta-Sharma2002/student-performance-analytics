"""
generate_data.py
-----------------
Generates a realistic synthetic dataset of 240 students across 3 sections,
5 subjects, plus study hours and attendance. Replaces the original 7-row
toy dataset with something that supports real statistical analysis
(correlations, distributions, cohort comparisons).
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan",
    "Krishna", "Ishaan", "Sweta", "Ananya", "Diya", "Aadhya", "Kavya", "Myra",
    "Sara", "Ira", "Pari", "Anika", "Rohan", "Kabir", "Dev", "Neha", "Priya",
    "Simran", "Tanvi", "Riya", "Aryan", "Yash", "Karan", "Meera", "Nisha",
    "Rahul", "Varun", "Sneha", "Pooja", "Amit", "Vikram", "Isha",
]
LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Rao", "Reddy",
    "Nair", "Iyer", "Chauhan", "Mehta", "Joshi", "Kapoor", "Malhotra",
    "Bhat", "Thakur", "Yadav", "Chopra", "Bose",
]

SECTIONS = ["A", "B", "C"]
SUBJECTS = ["Mathematics", "Science", "English", "Computer Science", "Social Studies"]

N_STUDENTS = 240

names = set()
while len(names) < N_STUDENTS:
    name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
    names.add(name)
names = list(names)
rng.shuffle(names)

rows = []
for i, name in enumerate(names):
    section = SECTIONS[i % 3]

    # Each student has an underlying "ability" level that correlates with
    # study hours, attendance, and scores -- mirrors how real cohorts behave.
    ability = rng.normal(0, 1)
    study_hours = np.clip(rng.normal(4 + ability * 1.2, 1.5), 0.5, 10)
    attendance = np.clip(rng.normal(85 + ability * 4, 8), 40, 100)

    scores = {}
    for subject in SUBJECTS:
        subject_noise = rng.normal(0, 6)
        score = 60 + ability * 12 + (study_hours - 4) * 3 + subject_noise
        scores[subject] = int(np.clip(round(score), 0, 100))

    rows.append({
        "StudentID": f"STU{i+1:04d}",
        "Name": name,
        "Section": section,
        **scores,
        "StudyHours": round(study_hours, 1),
        "Attendance": round(attendance, 1),
    })

df = pd.DataFrame(rows)
df.to_csv("data/students.csv", index=False)
print(f"Generated {len(df)} student records -> data/students.csv")
print(df.head())
