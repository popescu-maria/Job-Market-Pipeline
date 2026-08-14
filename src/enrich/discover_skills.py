import re
from collections import Counter

from src.ingestion.db import connect
from src.enrich.skills import clean_description

STOPWORDS = {
    "The", "We", "You", "Our", "This", "About", "Job", "Role",
    "Team", "Company", "We're", "If", "As", "In", "At", "For",
    "USA", "US", "UK", "EU",
}

def candidate_terms(text):
    # Capitalized words/acronyms
    words = re.findall(r"\b[A-Z][a-zA-Z0-9+#.]{1,20}\b", text)
    return [w for w in words if w not in STOPWORDS]


def main():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("SELECT description FROM jobs WHERE description IS NOT NULL")
        rows = cur.fetchall()
    conn.close()

    counter = Counter()
    for (description,) in rows:
        cleaned = clean_description(description)
        counter.update(candidate_terms(cleaned))

    print(f"Scanned {len(rows)} descriptions\n")
    print(f"{'term':<25} count")
    print("-" * 35)
    for term, count in counter.most_common(80):
        print(f"{term:<25} {count}")


if __name__ == "__main__":
    main()