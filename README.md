# Multi-Source Candidate Data Transformer

A Python-based data transformation pipeline developed as part of the **Eightfold Engineering Intern Assignment**.

The application ingests candidate information from multiple heterogeneous sources, normalizes inconsistent data, resolves conflicts using a deterministic merge strategy, validates the final profile, and generates a configurable canonical candidate profile with provenance tracking.

The pipeline is deterministic, modular, and configurable, ensuring the same input always produces the same canonical output.

---

# Features

- Parse candidate information from multiple sources
  - Recruiter CSV
  - GitHub JSON
  - Resume Text
- Normalize candidate information
  - Email
  - Phone Number
  - Name
  - Skills
- Identity Matching
- Conflict Resolution
- Canonical Candidate Profile Generation
- Provenance Tracking
- Confidence Scoring
- Runtime Configurable Output Projection
- Schema Validation

---

# Project Structure

```
candidate-data-transformer/

├── input/
│   ├── recruiter.csv
│   ├── github.json
│   └── resume.txt
│
├── modules/
│   ├── parser.py
│   ├── normalizer.py
│   ├── merger.py
│   ├── projector.py
│   └── validator.py
│
├── output/
│   └── candidate.json
│
├── tests/
│
├── config.json
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Pipeline Architecture

```
Input Sources
      │
      ▼
Parser
      │
      ▼
Normalization
      │
      ▼
Identity Matching
      │
      ▼
Conflict Resolution
      │
      ▼
Canonical Profile Generation
      │
      ▼
Validation
      │
      ▼
Projection Layer
      │
      ▼
Output JSON
```
---

## Design Principles

- Modular Architecture
- Deterministic Processing
- Explainable Merge Decisions
- Configurable Output
- Fault Tolerant
---

# Merge Strategy

Candidate records are merged using the following priority:

1. Normalized Email
2. Phone Number
3. Full Name + Current Company

Conflict Resolution Strategy

- Structured recruiter data is preferred when conflicts occur.
- Missing values are preserved instead of being inferred.
- Skills from GitHub and Resume are combined and deduplicated.
- Every selected field records its provenance.

---

# Normalization

The pipeline standardizes candidate information before merging.

Examples

| Raw Value | Normalized Value |
|-----------|------------------|
| Kanushka@GMAIL.COM | kanushka@gmail.com |
| 98765-43210 | +919876543210 |
| python | Python |
| PYTHON | Python |
| kanushka joshi | Kanushka Joshi |

---

# Canonical Schema

The internal canonical profile contains:

- candidate_id
- full_name
- emails
- phones
- location
- skills
- current_company
- title
- provenance
- overall_confidence

---

# Runtime Configurable Projection

The application separates the **internal canonical schema** from the **external output schema**.

The canonical profile internally stores:

```python
full_name
```

The output field name is controlled through **config.json**.

Example

```json
{
    "rename": {
        "full_name": "candidate_name"
    }
}
```

Without changing any Python code, the output becomes

```json
{
    "candidate_name": "Kanushka Joshi"
}
```

This keeps the business logic independent from client-specific output requirements.

---

# Provenance Tracking

Each selected field stores the source from which it was derived.

Example

```json
"provenance": {

    "email": {
        "sources": [
            "Recruiter CSV"
        ]
    },

    "skills": {
        "sources": [
            "GitHub",
            "Resume"
        ]
    }

}
```

This improves traceability and makes merge decisions transparent.

---

# Confidence Scoring

Source reliability scores:

| Source | Score |
|--------|------:|
| Recruiter CSV | 0.90 |
| GitHub | 0.75 |
| Resume | 0.60 |

The overall confidence score is calculated from the sources contributing to the final candidate profile.

---

# Example Transformation

## Input

### Recruiter CSV

```
Email : Kanushka@GMAIL.COM
Phone : 98765-43210
Company : Eightfold
```

### GitHub

```
Name : kanushka joshi
Skills : python, SQL, Machine Learning
```

### Resume

```
Skills

PYTHON
Machine Learning
Java
```

---

## Output

```
Candidate Name : Kanushka Joshi
Email : kanushka@gmail.com
Phone : +919876543210
Skills : Python, SQL, Java, Machine Learning
```

---

# How to Run

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd candidate-data-transformer
```

Run the application

```bash
python main.py
```

The generated canonical profile will be saved in

```
output/candidate.json
```
---

# Demo

### Pipeline Execution

![Pipeline Execution](assets/pipeline-run.png)

### Generated Canonical Profile

![Generated Canonical Profile](assets/output-json.png)

---

# Design Decisions

- Modular architecture separates parsing, normalization, merging, validation, and projection.
- Normalization is performed before merging to avoid duplicate or inconsistent values.
- The canonical schema remains independent of client-specific output formats.
- The projection layer uses configuration instead of code changes to customize output.
- Provenance is maintained for every merged field to improve traceability.
- Missing values are preserved rather than inferred.

---

# Assumptions

- One canonical profile is generated per candidate.
- Email is the preferred identity key.
- Resume contains identifiable section headings.
- Input files follow the expected sample formats.

---

# Future Improvements

- Support PDF and DOCX resume parsing.
- Fuzzy identity matching using similarity metrics.
- Database-backed candidate storage.
- REST API for profile transformation.
- Field-level confidence scoring.
- Support for additional data sources such as LinkedIn and ATS exports.
- Unit and integration tests.

---

# Author

**Kanushka Joshi**