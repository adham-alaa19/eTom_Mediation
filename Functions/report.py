import requests

TMF727_API_URL = "http://localhost:8000/tmf-api/serviceUsageManagement/v5/serviceUsage"

def report(record: dict) -> bool:
    try:
        response = requests.post(TMF727_API_URL, json=record)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[report] Failed to post record: {e}")
        return False
