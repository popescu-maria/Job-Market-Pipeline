import csv
import json

from fetch import fetch_jobs
from normalize import NORMALIZERS
from db import connect, upsert_job


def process_company(ats, slug, company):
    if ats not in NORMALIZERS:
        print(f"Skipping {company}: no normalizer for ats '{ats}'")
        return []

    raw_jobs = fetch_jobs(ats, slug)
    normalized = [NORMALIZERS[ats](job, company) for job in raw_jobs]
    return normalized


if __name__ == "__main__":
    all_jobs = []

    with open("config/sources.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                company_jobs = process_company(row["ats"], row["slug"], row["company"])
            except Exception as e:
                print(f"Error processing {row['company']}: {e}")
                continue
            print(f"{row['company']}: {len(company_jobs)} jobs")
            all_jobs.extend(company_jobs)

    conn = connect()
    for job in all_jobs:
        upsert_job(conn, job)
    conn.close()

    print(f"Wrote {len(all_jobs)} jobs to Postgres")