import hashlib

from modules.normalizer import (
    normalize_email,
    normalize_phone,
    normalize_name,
    normalize_skills,
)


def extract_resume_skills(resume_text):
    """
    Dynamically extract skills from the Skills section.
    Stops when another section begins.
    """
    skills = []
    in_skills = False

    stop_sections = {
        "education",
        "experience",
        "projects",
        "certifications",
        "languages",
        "interests"
    }

    for line in resume_text.splitlines():
        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # Start reading after "Skills"
        if lower == "skills":
            in_skills = True
            continue

        # Stop when next section starts
        if in_skills and lower in stop_sections:
            break

        if in_skills:
            skills.append(line)

    return skills


def calculate_confidence(profile):
    """
    Calculate confidence using the selected sources.
    """

    source_scores = {
        "Recruiter CSV": 0.90,
        "GitHub": 0.75,
        "Resume": 0.60,
    }

    used_sources = set()

    for value in profile["provenance"].values():

        if isinstance(value, dict):
            used_sources.update(value["sources"])

        else:
            used_sources.add(value)

    scores = [source_scores[s] for s in used_sources]

    return round(sum(scores) / len(scores), 2)


def merge_candidate(recruiter, github, resume_text):
    """
    Merge multiple candidate sources into one canonical profile.
    """

    # Dynamically extract skills from resume
    resume_skills = extract_resume_skills(resume_text)

    # # Apply normalization and merge strategy
    full_name = normalize_name(
        recruiter.get("full_name") or github.get("name")
    )

    email = normalize_email(
        recruiter.get("email") or github.get("email")
    )

    phone = normalize_phone(
        recruiter.get("phone")
    )

    skills = normalize_skills(
        github.get("languages", []) + resume_skills
    )

    primary_identifier = email or phone

    candidate_id = (
        hashlib.sha256(primary_identifier.encode()).hexdigest()
        if primary_identifier else None
    )

    canonical = {

        "candidate_id": candidate_id,

        "full_name": full_name,

        "emails": [email] if email else [],

        "phones": [phone] if phone else [],

        "location": github.get("location"),

        "skills": skills,

        "current_company": recruiter.get("current_company"),

        "title": recruiter.get("title"),

        "provenance": {

            "full_name": {
                "sources": ["Recruiter CSV"]
            },

            "email": {
                "sources": ["Recruiter CSV"]
            },

            "phone": {
                "sources": ["Recruiter CSV"]
            },

            "location": {
                "sources": ["GitHub"]
            },

            "skills": {
                "sources": ["GitHub", "Resume"]
            }

        }

    }

    canonical["overall_confidence"] = calculate_confidence(canonical)

    return canonical

def match_candidate(recruiter, github):

    if recruiter.get("email") and recruiter.get("email") == github.get("email"):
        return True

    if recruiter.get("phone") and recruiter.get("phone") == github.get("phone"):
        return True

    if (
        normalize_name(recruiter.get("full_name")) ==
        normalize_name(github.get("name"))
        and recruiter.get("current_company")
    ):
        return True

    return False

