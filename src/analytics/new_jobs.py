import sys
from datetime import datetime, timedelta, timezone

from src.ingestion.db import connect

def get_new_jobs(conn, since):
    sql = """
        SELECT source, company, title, location, url, first_seen_at
        FROM jobs
        WHERE first_seen_at >= %(since)s
          AND closed_at IS NULL
        ORDER BY first_seen_at DESC;
    """
    with conn.cursor() as cur:
        cur.execute(sql, {"since": since})
        return cur.fetchall()


if __name__ == "__main__":
    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    since = datetime.now(timezone.utc) - timedelta(hours=hours)

    conn = connect()
    jobs = get_new_jobs(conn, since)
    conn.close()

    print(f"{len(jobs)} new jobs in the last {hours}h:\n")
    for source, company, title, location, url, first_seen in jobs:
        print(f"[{company}] {title} — {location}")
        print(f"  {url}")
        print()