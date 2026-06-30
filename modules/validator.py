import re


def validate_profile(profile):
    """
    Validate the canonical candidate profile.
    """

    # Required fields
    required_fields = [
        "candidate_id",
        "full_name",
        "emails",
        "skills"
    ]

    for field in required_fields:
        if field not in profile or not profile[field]:
            raise ValueError(f"Missing required field: {field}")

    # Email validation
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    for email in profile["emails"]:
        if not re.match(email_pattern, email):
            raise ValueError(f"Invalid email: {email}")

    # Phone validation
    for phone in profile.get("phones", []):
        if not phone.startswith("+"):
            raise ValueError(f"Invalid phone: {phone}")

    # Skills must be a list
    if not isinstance(profile["skills"], list):
        raise ValueError("Skills must be a list")

    return True

