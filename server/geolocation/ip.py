import requests

PAYLOAD_KEYS = [
    "timezone"
]

def get_information_from_ip(ip: str):
    ip_info = {}

    if ip == "127.0.0.1":
        return {}
    
    resp = requests.get(f"https://ipapi.co/{ip}/json/")

    if resp.status_code == 200:
        payload = resp.json()

        if payload.get("error", False):
            return {}

        for key in PAYLOAD_KEYS:
            ip_info[key] = payload[key]

    return ip_info

