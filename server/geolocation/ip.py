import requests

# Defines the payload keys targeted to return.
PAYLOAD_KEYS = ["timezone"]


def get_information_from_ip(ip: str):
    """Makes a request to ipapi.co to get parsed information.

    Args:
        ip (str): The IP address to retrieve gathered information.

    Returns:
        A dict containing IP information from the payload based on defined keys.
        If ran from localhost, or an error occured in the API, return an empty dict.
    """

    ip_info = {}

    if ip != "127.0.0.1":
        resp = requests.get(f"https://ipapi.co/{ip}/json/")

        if resp.status_code == 200:
            payload = resp.json()

            if payload.get("error", False):
                return ip_info

            for key in PAYLOAD_KEYS:
                ip_info[key] = payload[key]

    return ip_info
