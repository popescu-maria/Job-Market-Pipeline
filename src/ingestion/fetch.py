import httpx

URL_TEMPLATES = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{slug}",
    "lever": "https://api.lever.co/v0/postings/{slug}?mode=json",
}   

def extract_greenhouse_jobs(data):
    return data["jobs"]

def extract_ashby_jobs(data):
    return data["jobs"]

def extract_lever_jobs(data):
    return data

JOB_EXTRACTORS = {
    "greenhouse": extract_greenhouse_jobs,
    "ashby": extract_ashby_jobs,
    "lever": extract_lever_jobs,
}

def build_url(ats, slug):
    if ats not in URL_TEMPLATES:
        raise ValueError(f"Unknown ATS: {ats}")
    return URL_TEMPLATES[ats].format(slug=slug)

async def fetch_jobs(ats, slug, client: httpx.AsyncClient):
    url = build_url(ats, slug)
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()
    return JOB_EXTRACTORS[ats](data)