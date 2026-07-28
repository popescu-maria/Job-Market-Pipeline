import httpx

URL_TEMPLATES = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{slug}",
}   

def build_url(ats, slug):
    if ats not in URL_TEMPLATES:
        raise ValueError(f"Unknown ATS: {ats}")
    return URL_TEMPLATES[ats].format(slug=slug)

def fetch_jobs(ats, slug):
    url = build_url(ats, slug)
    response = httpx.get(url)
    response.raise_for_status()
    data = response.json()
    return data["jobs"]

if __name__ == "__main__":
    ats = "greenhouse"
    slug = "grafanalabs"
    jobs = fetch_jobs(ats, slug)
    print(jobs[0]["title"]) 