import html
import re


SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "Golang", "SQL",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "Snowflake", "BigQuery", "Redshift", "Databricks", "ClickHouse",
    "Kafka", "Airflow", "dbt", "Spark", "Fivetran", "Parquet",
    "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Terraform", "GitLab", "GitHub Actions",
    "ETL", "ELT", "CI/CD",
]


def clean_description(text):
    if text is None:
        return None
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(description):
    if not description:
        return []
    cleaned = clean_description(description)
    text_lower = cleaned.lower()

    found = []
    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found