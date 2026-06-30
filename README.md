# 🤖 Redrob Ranker – AI Candidate Ranking System

> **An AI-powered candidate ranking pipeline for the Redrob INDIA RUNS Data & AI Challenge**

## 📌 Overview

Recruiters often sift through thousands of resumes to find the best candidates for a role. Traditional Applicant Tracking Systems (ATS) primarily rely on keyword matching, which frequently results in poor recommendations and can easily be fooled by keyword stuffing.

**Redrob Ranker** is an intelligent candidate ranking pipeline that ranks candidates the way an experienced recruiter would—by understanding career history, skill depth, behavioral signals, and semantic relevance rather than simply counting matching keywords.

Given a **Job Description** and approximately **100,000 candidate profiles**, the system generates a recruiter-friendly **Top 100 shortlist** with interpretable scores and reasoning.

---

# 🎯 Problem Statement

Traditional hiring systems suffer from several limitations:

* Keyword matching ignores actual experience.
* Candidates can manipulate rankings by keyword stuffing.
* Career progression and skill depth are often ignored.
* Recruiters spend excessive time manually reviewing resumes.

This project addresses these problems using a multi-stage AI pipeline that combines semantic retrieval, feature engineering, recruiter-inspired scoring, and honeypot detection.

---

# 🏗️ System Architecture

```
                   Job Description
                          │
                          ▼
              Stage 1 – JD Understanding
                          │
                          ▼
                jd_requirements.json
                          │
                          │
Candidates.jsonl ─────────┘
        │
        ▼
 Stage 2 – Candidate Representation
        │
        ▼
candidate_features_full.jsonl
        │
        ▼
 Stage 3 – Hybrid Retrieval
      100,000 → 3,000
        │
        ▼
 Stage 4 – Candidate Scoring
        │
        ▼
 Stage 5 – Honeypot Detection
        │
        ▼
 Stage 6 – Reasoning Generation
        │
        ▼
      submission.csv
```

---

# 🚀 Features

* Intelligent Job Description Understanding
* Semantic Candidate Matching
* Hybrid Retrieval (Embeddings + BM25)
* Career Trajectory Analysis
* Skill Depth Evaluation
* Hireability Assessment
* Honeypot / Fake Profile Detection
* Recruiter-Friendly Reasoning Generation
* CPU Optimized Pipeline
* Offline Execution (No Internet Required After Initial Setup)

---

# 📂 Project Structure

```
redrob-ranker/
│
├── rank.py                     # Main pipeline entry point
├── submission.csv
│
├── scripts/
│   ├── run_stage1.py
│   ├── run_stage2.py
│   ├── run_stage3.py
│   ├── run_stage5.py
│   └── run_stage6.py
│
├── src/
│   ├── jd_parser.py
│   ├── candidate_features.py
│   ├── retrieval.py
│   ├── scoring.py
│   ├── honeypot.py
│   ├── reasoning.py
│   ├── constants.py
│   └── candidate_loader.py
│
├── data/
│   └── precomputed/
│       ├── jd_requirements.json
│       ├── candidate_features_full.jsonl
│       ├── candidate_embeddings.npy
│       ├── retrieved_top3000.jsonl
│       ├── honeypot_assessments.jsonl
│       └── scored_top100.jsonl
│
app.py           # Streamlit Sandbox
|
requirements.txt
|
Readme.md                 
```

---

# ⚙️ Pipeline Explanation

## Stage 1 — Job Description Understanding

The job description is parsed into structured recruiter requirements.

Extracted information includes:

* Role Title
* Role Family
* Experience Band
* Must-Have Skills
* Preferred Locations
* Soft Skills
* Disqualifiers

Output:

```
jd_requirements.json
```

---

## Stage 2 — Candidate Representation

Each candidate profile is transformed into:

### Canonical Text

```
Headline
Summary
Current Title
Career Descriptions
Skills
```

### Structured Features

* Role Fit
* Skill Depth
* Career Progression
* Skill Verification
* Hireability
* Behavioral Signals
* Authenticity

Output:

```
candidate_features_full.jsonl
```

---

## Stage 3 — Hybrid Retrieval

Instead of scoring every candidate, the system first retrieves the most relevant candidates.

Retrieval Score:

```
0.6 × Semantic Similarity
+
0.4 × BM25
```

Technologies:

* Sentence Transformers
* MiniLM Embeddings
* BM25

Output:

```
retrieved_top3000.jsonl
```

---

## Stage 4 — Recruiter Inspired Scoring

Each retrieved candidate receives an interpretable score.

```
Score =
Semantic Fit
+ Career Trajectory
+ Skill Trust
+ Hireability
− Inconsistency
− Keyword Stuffing
− Honeypot Penalties
```

Career history is intentionally weighted higher than raw skill count.

---

## Stage 5 — Honeypot Detection

The challenge dataset intentionally contains misleading candidate profiles.

Examples:

* AI skills with non-technical career history
* Copied job descriptions
* Title and experience mismatch
* Endorsement and assessment inconsistencies

These profiles receive penalties to prevent keyword gaming.

---

## Stage 6 — Reasoning Generation

Every shortlisted candidate includes recruiter-readable reasoning.

Example:

```
Senior AI Engineer with 7.8 years experience;
Hybrid Retrieval in production;
11 verified skills;
Response rate 0.76.
```

---

# 🧠 Technologies Used

* Python 3.11
* NumPy
* Pandas
* Sentence Transformers
* all-MiniLM-L6-v2
* rank-bm25
* python-docx
* JSON
* Streamlit

---

# 💻 Installation

## Clone Repository

```bash
git clone https://github.com/karthik-51/Team_Code_Crusaders.git

```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```
```bash
cd redrob-ranker
```
---

# 📁 Dataset

Project layout assumes:

```
/redrob-ranker/dataset/

├── candidates.jsonl
├── sample_candidates.json
├── validate_submission.py
└── job_description.docx
```

---

# ▶️ Running the Pipeline

## Recommended (Fast Execution)

Uses precomputed artifacts.

```bash
python rank.py --skip-stage1 --skip-stage2 --skip-stage3
```

This executes:

* Stage 5
* Stage 6

Output:

```
submission.csv
```

---

## Full Pipeline

```bash
python rank.py
```

Runs:

* Stage 1
* Stage 2
* Stage 3
* Stage 5
* Stage 6

---

# 🧪 Running Individual Stages

## Stage 1

```bash
python scripts/run_stage1.py --jd data/job_description.txt
```

---

## Stage 2

```bash
python scripts/run_stage2.py
```

---

## Stage 3

```bash
python scripts/run_stage3.py
```

---

## Stage 5

```bash
python scripts/run_stage5.py
```

---

## Stage 6

```bash
python scripts/run_stage6.py
```

---

# ✅ Validate Submission

```bash
python dataset/validate_submission.py submission.csv
```

A valid submission must:

* Contain exactly 100 candidates
* Have non-increasing scores
* Use UTF-8 encoding
* Follow the required CSV format

---

# 🌐 Streamlit Demo

Streamlit Live Link:

```bash
https://teamcodecrusaders-redrob.streamlit.app/
```

Launch locally:

```bash
streamlit run ../app.py
```

The web application allows users to:

* Upload Candidate Dataset
* Run Ranking Pipeline
* View Top Candidates
* Download csv

---

# 📊 Performance

| Pipeline Stage     | Approximate Runtime |
| ------------------ | ------------------- |
| JD Parsing         | < 5 sec             |
| Feature Extraction | Depends on dataset  |
| Retrieval          | ~1 minute           |
| Scoring            | < 30 sec            |
| Reasoning          | < 10 sec            |

Subsequent runs are significantly faster because embeddings and intermediate features are cached.

---

# 📌 Design Principles

* Recruiter-inspired ranking instead of keyword matching
* Explainable scoring
* Career history prioritized over skill count
* Offline execution
* Modular architecture
* Fast CPU inference
* Cached intermediate artifacts
* Explicit honeypot detection

---

# 📄 Output

The final output is:

```
submission.csv
```

Format:

```
candidate_id,rank,score,reasoning
```

Example:

```
CAND_001,1,0.9920,"Senior AI Engineer with 7.8 yrs; hybrid retrieval in production; 11 verified skills."
```

---

# 📈 Future Improvements

* Learning-to-Rank (LightGBM Ranker)
* Graph-based Career Embeddings
* LLM-assisted Reasoning
* Interactive Recruiter Dashboard
* Multi-JD Batch Ranking
* Explainable Feature Visualization

---

# 👨‍💻 Author

**V. Laxmi Narayan Sharma**

M.Tech Computer Science & Engineering

Specialization:

* Artificial Intelligence
* Machine Learning
* Information Security
* Intelligent Systems

---

# 📜 License

This repository is intended for educational purposes and submission to the Redrob INDIA RUNS Data & AI Challenge.

Please refer to the competition rules before reusing any dataset or challenge assets.