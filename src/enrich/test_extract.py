from src.ingestion.db import connect
from src.enrich.skills import extract_skills


def main():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT title, company, description
            FROM jobs
            WHERE description IS NOT NULL
            LIMIT 5
        """)
        rows = cur.fetchall()
    conn.close()

    for title, company, description in rows:
        skills = extract_skills(description)
        print(f"[{company}] {title}")
        print(f"  Skills: {skills}")
        print()


if __name__ == "__main__":
    main()