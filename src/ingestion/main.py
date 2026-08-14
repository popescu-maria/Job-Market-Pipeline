import asyncio
import csv
import time

import httpx

from datetime import datetime, timezone
from src.ingestion.fetch import fetch_jobs
from src.ingestion.normalize import NORMALIZERS
from src.ingestion.db import connect, upsert_jobs, mark_closed_jobs
from src.enrich.skills import extract_skills

async def process_company(ats, slug, company, client):
    if ats not in NORMALIZERS:
        print(f"Skipping {company}: no normalizer for ats '{ats}'")
        return False, []

    try:
        raw_jobs = await fetch_jobs(ats, slug, client)
    except Exception as e:
        print(f"Error processing {company}: {e}")
        return False, []

    normalized = [NORMALIZERS[ats](job, company) for job in raw_jobs]
    for job in normalized:
        job["skills"] = extract_skills(job.get("description"))

    print(f"{company}: {len(normalized)} jobs")
    return True, normalized


async def main():
    run_started_at = datetime.now(timezone.utc)
    
    with open("config/sources.csv", newline="") as f:
        rows = list(csv.DictReader(f))

    async with httpx.AsyncClient() as client:
        tasks = [
            process_company(row["ats"], row["slug"], row["company"], client)
            for row in rows
        ]
        results = await asyncio.gather(*tasks)

    all_jobs = []
    successful_sources = []

    for row, (succeeded, jobs) in zip(rows, results):
        all_jobs.extend(jobs)
        if succeeded:
            successful_sources.append((row["ats"], row["company"]))

    conn = connect()
    upsert_jobs(conn, all_jobs)
    mark_closed_jobs(conn, successful_sources, run_started_at)
    conn.close()

    print(f"\nWrote {len(all_jobs)} jobs to Postgres")


if __name__ == "__main__":
    start = time.time()

    asyncio.run(main())

    elapsed = time.time() - start

    print(f"Elapsed time: {elapsed:.2f} seconds")