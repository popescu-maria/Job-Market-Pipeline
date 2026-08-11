import asyncio
import csv
import time

import httpx

from fetch import fetch_jobs
from normalize import NORMALIZERS
from db import connect, upsert_jobs


async def process_company(ats, slug, company, client):
    if ats not in NORMALIZERS:
        print(f"Skipping {company}: no normalizer for ats '{ats}'")
        return []

    try:
        raw_jobs = await fetch_jobs(ats, slug, client)
    except Exception as e:
        print(f"Error processing {company}: {e}")
        return []

    normalized = [NORMALIZERS[ats](job, company) for job in raw_jobs]
    print(f"{company}: {len(normalized)} jobs")
    return normalized


async def main():
    with open("config/sources.csv", newline="") as f:
        rows = list(csv.DictReader(f))

    async with httpx.AsyncClient() as client:
        tasks = [
            process_company(row["ats"], row["slug"], row["company"], client)
            for row in rows
        ]
        results = await asyncio.gather(*tasks)

    all_jobs = [job for company_jobs in results for job in company_jobs]

    conn = connect()
    upsert_jobs(conn, all_jobs)
    conn.close()

    print(f"\nWrote {len(all_jobs)} jobs to Postgres")


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    elapsed = time.time() - start
    print(f"Elapsed time: {elapsed:.2f} seconds")