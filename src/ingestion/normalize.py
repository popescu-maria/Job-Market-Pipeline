import json

def normalize_greenhouse_job(raw_job, company):
    return {
        "external_id": raw_job["id"],
        "title": raw_job["title"],
        "location": raw_job["location"]["name"],
        "url": raw_job["absolute_url"],
        "company": company,
        "source": "greenhouse",
        "posted_at": raw_job["first_published"],
    }

def normalize_ashby_job(raw_job, company):
    return {
        "external_id": raw_job["id"],
        "title": raw_job["title"],
        "location": raw_job["location"],
        "url": raw_job["jobUrl"],
        "company": company,
        "source": "ashby",
        "posted_at": raw_job["publishedAt"],
    }

NORMALIZERS = {
    "greenhouse": normalize_greenhouse_job,
    "ashby": normalize_ashby_job,
}

if __name__ == "__main__":
    import httpx


    # response = httpx.get("https://api.ashbyhq.com/posting-api/job-board/uipath")
    response = httpx.get("https://boards-api.greenhouse.io/v1/boards/grafanalabs/jobs")

    data = response.json()
    job = data["jobs"][0]

    normalized_job = NORMALIZERS["greenhouse"](job, "Grafana Labs")
    print(json.dumps(normalized_job, indent=2))