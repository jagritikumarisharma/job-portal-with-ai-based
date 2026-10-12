
import os, re, json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from matching import extract_text_from_file, score_resume

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
DATA_DIR = "data"
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def load_jobs():
    try:
        with open(JOBS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_jobs(jobs):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    jobs = load_jobs()
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    if q:
        jobs = [j for j in jobs if q in (j["title"] + " " + j["company"] + " " + j["description"] + " " + j["skills"]).lower()]
    if category:
        jobs = [j for j in jobs if j.get("category", "") == category]
    categories = sorted({j.get("category", "Other") for j in load_jobs()})
    return render_template("index.html", jobs=jobs, q=request.args.get("q", ""), category=category, categories=categories)

@app.route("/job/<int:job_id>")
def job_detail(job_id):
    job = next((j for j in load_jobs() if j["id"] == job_id), None)
    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("index"))
    return render_template("job_detail.html", job=job)

@app.route("/post-job", methods=["GET", "POST"])
def post_job():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "Other").strip()
        skills = request.form.get("skills", "").strip()
        description = request.form.get("description", "").strip()
        if not all([title, company, location, skills, description]):
            flash("Please fill in all required fields.", "error")
            return render_template("post_job.html", form=request.form)
        jobs = load_jobs()
        next_id = max([j["id"] for j in jobs], default=0) + 1
        jobs.insert(0, {
            "id": next_id, "title": title, "company": company, "location": location,
            "category": category, "skills": skills, "description": description,
            "posted": datetime.now().strftime("%d %b %Y")
        })
        save_jobs(jobs)
        flash("Job posted successfully.", "success")
        return redirect(url_for("job_detail", job_id=next_id))
    return render_template("post_job.html", form={})

@app.route("/match", methods=["GET", "POST"])
def match():
    jobs = load_jobs()
    results = []
    resume_text = ""
    if request.method == "POST":
        uploaded = request.files.get("resume")
        pasted = request.form.get("resume_text", "").strip()
        if uploaded and uploaded.filename:
            if not allowed_file(uploaded.filename):
                flash("Please upload a PDF, DOCX, or TXT file.", "error")
            else:
                filename = secure_filename(uploaded.filename)
                stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                path = os.path.join(app.config["UPLOAD_FOLDER"], stamp + "_" + filename)
                uploaded.save(path)
                try:
                    resume_text = extract_text_from_file(path, filename)
                except Exception as exc:
                    resume_text = ""
                    flash("Could not read this file. Try a text-based PDF/DOCX or paste your resume text.", "error")
                finally:
                    try:
                        os.remove(path)
                    except OSError:
                        pass
        elif pasted:
            resume_text = pasted
        else:
            flash("Upload your resume or paste its text to continue.", "error")
        if resume_text.strip():
            for job in jobs:
                combined = f'{job["title"]}. Required skills: {job["skills"]}. {job["description"]}'
                score, matched, missing = score_resume(resume_text, combined, job["skills"])
                results.append({"job": job, "score": score, "matched": matched, "missing": missing})
            results.sort(key=lambda item: item["score"], reverse=True)
    return render_template("match.html", results=results, resume_text=resume_text)

@app.errorhandler(RequestEntityTooLarge)
def too_large(_error):
    flash("File is too large. Maximum upload size is 5 MB.", "error")
    return redirect(url_for("match"))

if __name__ == "__main__":
    app.run(debug=True)
