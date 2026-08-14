import psycopg
import os

from dotenv import load_dotenv
from psycopg.types.json import Jsonb

load_dotenv()

def connect():
    return psycopg.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
    )

UPSERT_SQL = """
    INSERT INTO jobs (source, external_id, title, location, url, company, posted_at, description, skills, raw_json, last_seen_at)
    VALUES (%(source)s, %(external_id)s, %(title)s, %(location)s, %(url)s, %(company)s, %(posted_at)s, %(description)s, %(skills)s, %(raw_json)s, now())
    ON CONFLICT (source, external_id) DO UPDATE SET
        title = EXCLUDED.title,
        location = EXCLUDED.location,
        url = EXCLUDED.url,
        posted_at = EXCLUDED.posted_at,
        description = EXCLUDED.description,
        skills = EXCLUDED.skills,
        raw_json = EXCLUDED.raw_json,
        closed_at = NULL,
        last_seen_at = now();
"""


def upsert_jobs(conn, jobs):
    jobs_for_db = [{**job, "raw_json": Jsonb(job["raw_json"])} for job in jobs]
    with conn.cursor() as cur:
        cur.executemany(UPSERT_SQL, jobs_for_db)
    conn.commit()


def mark_closed_jobs(conn, successful_sources, run_started_at):
    if not successful_sources:
        return

    placeholders = ", ".join(["(%s, %s)"] * len(successful_sources))
    sql = f"""
        UPDATE jobs
        SET closed_at = now()
        WHERE closed_at IS NULL
          AND last_seen_at < %s
          AND (source, company) IN ({placeholders})
    """

    params = [run_started_at]
    for ats, company in successful_sources:
        params.append(ats)
        params.append(company)

    with conn.cursor() as cur:
        cur.execute(sql, params)
        print(f"Marked {cur.rowcount} jobs as closed")
    conn.commit()