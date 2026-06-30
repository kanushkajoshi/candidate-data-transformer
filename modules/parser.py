import csv
import json


def parse_recruiter_csv(file_path):
    """Read recruiter CSV and return a dictionary."""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return next(reader)


def parse_github_json(file_path):
    """Read GitHub profile JSON."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_resume_txt(file_path):
    """Read resume text."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()