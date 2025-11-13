# 🧠 Smart Resume Screener — AI-Powered Resume Matching Tool

A fully automated **AI-powered resume screening system** built with **Python, NLP, Machine Learning, and Streamlit**. This tool extracts text from resumes (PDF/DOCX), identifies skills using NLP, matches them with a given Job Description (JD), computes a score (0–100), and highlights matched/missing skills. The app also supports **bulk resume uploads** and generates CSV summaries.

This project is production-ready and publicly deployed on **Streamlit Cloud**.

---

## 🚀 Live Demo

👉 **App Link:** *https://smart-resume-screener-by-garvit-rastogi.streamlit.app/*

---

## 📂 GitHub Repository

👉 **Repo Link:** *Add your GitHub repo link here*

---

# 📘 Table of Contents

* [✨ Features](#-features)
* [🧰 Tech Stack](#-tech-stack)
* [📁 Project Structure](#-project-structure)
* [⚙️ Installation (Local Setup)](#️-installation-local-setup)
* [▶️ Run Locally](#️-run-locally)
* [🧠 Core Logic & Algorithms](#-core-logic--algorithms)
* [📊 Output & Interpretation](#-output--interpretation)
* [🌐 Deployment Guide (Streamlit Cloud)](#-deployment-guide-streamlit-cloud)
* [📈 Future Enhancements](#-future-enhancements)
* [🤝 Contributing](#-contributing)
* [📜 License](#-license)

---

# ✨ Features

### ✅ **1. Single Resume Screening**

Upload a PDF/DOCX resume → get:

* Extracted text & skills
* Required skills from JD
* Match score (**0–100**)
* JD similarity %
* Skill coverage %
* Missing skill list
* Downloadable CSV

### ✅ **2. Bulk Screening**

Upload multiple resumes →

* Auto-ranked table by score
* PASS/REJECT classification
* Full CSV export

### ✅ **3. NLP-Powered Skill Extraction**

* Uses **spaCy PhraseMatcher** + fuzzy matching
* Customizable `skills_list.txt`

### ✅ **4. Intelligent Scoring**

Score = `0.6 * JD_similarity + 0.4 * Skill_coverage` (adjustable)

* JD similarity: TF-IDF cosine
* Skill coverage: % of JD skills present in resume

### ✅ **5. Fully Deployable**

Runs locally or on **Streamlit Cloud** with free hosting.

---

# 🧰 Tech Stack

| Component      | Technology                               |
| -------------- | ---------------------------------------- |
| Language       | Python 3.x                               |
| NLP            | spaCy, PhraseMatcher, rapidfuzz          |
| ML             | scikit-learn (TF‑IDF, cosine similarity) |
| Resume Parsing | pdfplumber, python-docx                  |
| Web App        | Streamlit                                |
| Deployment     | Streamlit Community Cloud                |

---

# 📁 Project Structure

```
smart-resume-screener/
│
├── app.py                    # Streamlit UI
├── requirements.txt          # Dependencies
├── skills_list.txt           # Skills dictionary
│
├── src/
│   ├── parse_resume.py       # PDF/DOCX parsing
│   ├── nlp_utils.py          # NLP preprocessing + matcher builder
│   ├── matcher.py            # Skill extraction logic
│   └── scoring.py            # TF‑IDF & scoring functions
│
├── sample_resumes/           # (Optional) Test resumes
├── results/                  # Auto-generated CSVs (ignored in repo)
└── README.md
```

---

# ⚙️ Installation (Local Setup)

### 1️⃣ Clone the repo

```bash
git clone <your-github-repo-url>
cd smart-resume-screener
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download spaCy model

```bash
python -m spacy download en_core_web_sm
```

---

# ▶️ Run Locally

```bash
streamlit run app.py
```

Open browser → `http://localhost:8501`

---

# 🧠 Core Logic & Algorithms

### 1️⃣ **Resume Parsing**

* `pdfplumber` → extract PDF text
* `python-docx` → extract DOCX text
* Automatic cleaning and normalization

### 2️⃣ **NLP Processing**

* Convert text → spaCy Doc
* Remove stopwords, punctuation
* Lemmatize tokens

### 3️⃣ **Skill Extraction**

#### Using PhraseMatcher

Matches exact phrases from `skills_list.txt`.

#### Using RapidFuzz Fuzzy Matching

Handles:

* Misspellings
* Partial matches
* Multi-word variations

### 4️⃣ **Scoring**

Score is calculated as:

```
final_score = 0.6 * jd_similarity + 0.4 * skill_coverage
```

Where:

* `jd_similarity` = cosine similarity of TF‑IDF vectors
* `skill_coverage` = matched_required_skills / total_required_skills

Converted to percentage 0–100 in UI.

---

# 📊 Output & Interpretation

### For each resume, output includes:

* **Match Score (0–100) ✓**
* **JD Similarity %**
* **Skill Coverage %**
* **Required Skills**
* **Matched Skills**
* **Missing Skills**
* **Download CSV Report**

### For bulk upload:

* Ranked table (descending score)
* PASS/REJECT (based on threshold slider)
* Downloadable CSV summary

---

# 🌐 Deployment Guide (Streamlit Cloud)

### 1️⃣ Push project to GitHub

Include:

* `app.py`
* `requirements.txt`
* `src/`
* `skills_list.txt`

### 2️⃣ Go to Streamlit Cloud

🔗 [https://streamlit.io/cloud](https://streamlit.io/cloud)

### 3️⃣ Connect GitHub → Deploy new app

* Choose your repo
* File path: `app.py`
* Deploy

### 4️⃣ Add spaCy model auto-download (if needed)

Included in `app.py` safe-loader:

```python
try:
    nlp = spacy.load("en_core_web_sm")
except:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
```

### 5️⃣ Get public link → share

Your app is now live globally.

---

# 📈 Future Enhancements

* 🔍 Use **SentenceTransformer embeddings** for better semantic similarity
* 🌐 Add **FastAPI backend** for production
* 👤 Add user session login/authentication
* 📄 Add section-based parsing (Experience, Education, etc.)
* 📌 ATS-format resume export
* 🏷️ Add named entity recognition for:

  * Companies
  * Titles
  * Dates
  * Locations

---

# 🤝 Contributing

Pull requests are welcome. For major changes, open an issue to discuss what you’d like to improve.

---

# 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

# 🙌 Credits

Built using:

* Streamlit
* spaCy
* scikit-learn
* rapidfuzz
* pdfplumber / python-docx

Developed by: **Garvit Rastogi**

---
