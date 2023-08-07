import pytest
import requests
from geolocation.ip import get_information_from_ip


class MockResponse:
    IP_RESULTS = {
        "123.45.67.89": {
            "status": 200,
            "results": {
                "timezone": "America/New_York",
                "extra_key": True,
            },
        },
        "1.1.1.1": {
            "status": 200,
            "results": {"timezone": "Europe/London", "error": True},
        },
        "10.10.10.10": {
            "status": 500,
            "results": {"nothing_expected": True},
        },
        "255.255.255.255": {
            "status": 200,
            "results": {"missing_timezone": True},
        },
    }

    def __init__(self, url):
        self.ip = url.split("/")[3]

    @property
    def status_code(self):
        return self.IP_RESULTS[self.ip]["status"]

    def json(self):
        return self.IP_RESULTS[self.ip]["results"]


@pytest.fixture
def mock_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(*args)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.mark.parametrize(
    "ip, res, err",
    [
        ("127.0.0.1", {}, None),
        ("123.45.67.89", {"timezone": "America/New_York"}, None),
        ("1.1.1.1", {}, None),
        ("10.10.10.10", {}, None),
        ("255.255.255.255", None, KeyError),
    ],
)
def test_get_information_from_ip(ip, res, err, mock_response):
    print(ip, res, err, mock_response)
    if err:
        with pytest.raises(err):
            get_information_from_ip(ip)
    else:
        ip_info = get_information_from_ip(ip)
        assert ip_info == res
