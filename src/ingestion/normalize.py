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
        "raw_json": raw_job,
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
        "raw_json": raw_job,
    }


def normalize_lever_job(raw_job, company):
    return {
        "external_id": raw_job["id"],
        "title": raw_job["text"],
        "location": raw_job["categories"]["location"],
        "url": raw_job["hostedUrl"],
        "company": company,
        "source": "lever",
        "posted_at": raw_job["createdAt"],
        "raw_json": raw_job,
    }


NORMALIZERS = {
    "greenhouse": normalize_greenhouse_job,
    "ashby": normalize_ashby_job,
    "lever": normalize_lever_job,
}