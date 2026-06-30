import json

from modules.parser import (
    parse_recruiter_csv,
    parse_github_json,
    parse_resume_txt,
)

from modules.merger import match_candidate, merge_candidate
from modules.validator import validate_profile
from modules.projector import project_profile


def main():

    print("=" * 60)
    print(" Multi-Source Candidate Data Transformer Pipeline")
    print("=" * 60)

    print("\n[1/7] Reading recruiter CSV...")
    recruiter = parse_recruiter_csv("input/recruiter.csv")

    print("[2/7] Reading GitHub profile...")
    github = parse_github_json("input/github.json")

    print("[3/7] Reading resume...")
    resume = parse_resume_txt("input/resume.txt")

    print("[4/7] Matching candidate identities...")

    if not match_candidate(recruiter, github):
        raise ValueError("Candidate records do not match.")

    print("[5/7] Merging candidate profiles...")
    profile = merge_candidate(recruiter, github, resume)

    print("[6/7] Validating canonical profile...")
    validate_profile(profile)

    print("[7/7] Applying runtime projection...")

    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    output = project_profile(profile, config)

    with open("output/candidate.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)

    print("\n✅ Candidate profile generated successfully!\n")

    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()