import json

from fetch import fetch_jobs
from normalize import NORMALIZERS

def test_company(ats, slug, company):
    jobs = fetch_jobs(ats, slug)
    job = jobs[0]
    normalized_job = NORMALIZERS[ats](job, company)
    print(json.dumps(normalized_job, indent=2))

if __name__ == "__main__":
    test_company("greenhouse", "grafanalabs", "Grafana Labs")
    test_company("ashby", "uipath", "UiPath")