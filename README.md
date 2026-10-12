
# CareerMatch AI — Job Portal with AI-Based Resume Matching

A final-semester BCA/B.Tech/MCA-style web project built with **Python, Flask, scikit-learn, HTML, and CSS**. It includes a job board, job posting form, resume upload/text input, and explainable job-to-resume matching.

## Features

- Browse, search, and filter sample job listings.
- View job details and required skills.
- Post a new job (stored in `data/jobs.json`).
- Upload a PDF, DOCX, or TXT resume (maximum 5 MB), or paste resume text.
- Rank available jobs by a matching score.
- Show exact matched and missing required skills.
- Responsive UI and sample data to make the demo easy to present.
- Uploaded files are deleted after extraction; extracted resume text is not saved by the app.

## How the matching works

The baseline matcher combines:
1. **TF-IDF + cosine similarity** between resume text and job title/skills/description (65% of score).
2. **Required-skill coverage** from the comma-separated skills field (35% of score).

This is an explainable, lightweight NLP baseline—not a large language model. The score is approximate, and exact skill matching may miss synonyms (e.g., “JS” vs “JavaScript”). It must not be used as the sole basis for real hiring decisions.

## Requirements

- Python 3.10 or newer recommended
- pip
- Internet is only needed if your browser loads the optional Google Fonts stylesheet; the application itself runs locally.

## Run on Windows

1. Extract the ZIP folder.
2. Open the extracted `ai_job_portal` folder in VS Code.
3. Open Terminal in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the app:
   ```bash
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

## Run on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

## Project structure

```text
ai_job_portal/
├── app.py                 # Flask routes and application logic
├── matching.py            # Resume text extraction and scoring
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   └── jobs.json          # Sample jobs; new jobs are saved here
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── job_detail.html
│   ├── post_job.html
│   └── match.html
└── static/
    ├── style.css
    └── uploads/           # Temporary upload directory
```

## Demo walkthrough

1. Open the home page and explore the five sample jobs.
2. Click **Post a Job** and add a sample role.
3. Open **Resume Match**.
4. Paste sample resume text or upload a text-based PDF/DOCX/TXT file.
5. Review ranked roles and matched/missing skills.

Example resume text for testing:

```text
Computer Science student with project experience in Python, Flask, SQL, Git,
REST API development, HTML, CSS, JavaScript, Pandas and scikit-learn.
Built a student management system and a data analysis dashboard.
Familiar with object-oriented programming, data structures and responsive design.
```

## Important limitations / future scope

- This is an academic demo; authentication, email alerts, employer verification, and production deployment are not included.
- Jobs are stored in a JSON file rather than a production database.
- For a stronger version, add SQLite/PostgreSQL, login/roles, an admin dashboard, automated tests, resume synonym handling, and a consent-aware privacy policy.
- Do not expose the Flask development server directly to the public internet. Set a strong `SECRET_KEY` and use a production WSGI server before deployment.

## Suggested final-semester report chapters

1. Introduction and problem statement
2. Literature review / existing system
3. Proposed system and objectives
4. Requirements and feasibility
5. System design (use-case, activity, ER/data-flow diagrams)
6. Implementation and matching algorithm
7. Testing and results
8. Limitations, conclusion, and future scope
