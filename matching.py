
import os, re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = {
    "the","and","for","with","you","your","are","was","were","this","that","from","have","has",
    "will","our","their","they","them","his","her","she","him","but","not","all","can","able",
    "into","about","who","what","when","where","which","while","also","using","use","used","work",
    "working","experience","years","year","role","team","job","skills","skill","good","strong",
    "required","preferred","knowledge","ability","responsibilities","candidate","including"
}

def normalize(text):
    return re.sub(r"\s+", " ", (text or "").lower()).strip()

def extract_keywords(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.]{1,}", normalize(text))
    return sorted({w.strip(".") for w in words if len(w.strip(".")) > 1 and w not in STOPWORDS})

def score_resume(resume_text, job_text, skill_string=""):
    """Explainable baseline matcher: TF-IDF similarity + explicit required-skill overlap."""
    resume = normalize(resume_text)
    job = normalize(job_text)
    try:
        matrix = TfidfVectorizer(ngram_range=(1, 2), stop_words="english").fit_transform([resume, job])
        similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        similarity = 0.0
    required = [s.strip().lower() for s in re.split(r"[,;\n]", skill_string) if s.strip()]
    matched = [s for s in required if re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", resume)]
    missing = [s for s in required if s not in matched]
    skill_ratio = len(matched) / max(1, len(required))
    # Similarity contributes 65%, listed skill coverage contributes 35%.
    score = round(min(100, max(0, (similarity * 65 + skill_ratio * 35))))
    return score, matched, missing

def extract_text_from_file(path, original_filename):
    ext = original_filename.rsplit(".", 1)[1].lower()
    if ext == "txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if ext == "pdf":
        from pypdf import PdfReader
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == "docx":
        from docx import Document
        document = Document(path)
        return "\n".join(p.text for p in document.paragraphs)
    raise ValueError("Unsupported file type")
