import re


def normalize_email(email):
    """Convert email to lowercase and remove extra spaces."""
    if not email:
        return None
    return email.strip().lower()


def normalize_phone(phone):
    """Keep only digits and convert to E.164 format."""
    if not phone:
        return None

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 10:
        digits = "91" + digits

    return "+" + digits


def normalize_name(name):
    """Convert name to title case."""
    if not name:
        return None
    return name.strip().title()


def normalize_skills(skills):
    """Remove duplicates and normalize skill names."""
    if not skills:
        return []

    canonical = {
        "python": "Python",
        "java": "Java",
        "sql": "SQL",
        "machine learning": "Machine Learning",
        "ml": "Machine Learning"
    }

    normalized = []

    for skill in skills:
        key = skill.strip().lower()
        normalized.append(canonical.get(key, skill.title()))

    return list(dict.fromkeys(normalized))