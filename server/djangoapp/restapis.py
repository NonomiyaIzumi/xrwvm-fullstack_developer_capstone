"""
Thin HTTP client used by djangoapp views to talk to the two capstone
microservices: the Node.js/Express + MongoDB dealer/review service and the
Flask sentiment-analysis service. Both base URLs come from settings so the
same code works locally and against a deployment.
"""

from urllib.parse import urlencode

import requests
from django.conf import settings


def get_request(endpoint, **kwargs):
    params = urlencode(kwargs)
    url = f"{settings.BACKEND_URL}{endpoint}"
    if params:
        url = f"{url}?{params}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"restapis.get_request error for {url}: {error}")
        return {"error": str(error)}


def post_request(endpoint, json_payload, **kwargs):
    params = urlencode(kwargs)
    url = f"{settings.BACKEND_URL}{endpoint}"
    if params:
        url = f"{url}?{params}"
    try:
        response = requests.post(url, json=json_payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"restapis.post_request error for {url}: {error}")
        return {"error": str(error)}


def analyze_review_sentiments(text):
    url = f"{settings.SENTIMENT_ANALYZER_URL}/analyze/{requests.utils.quote(text)}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"restapis.analyze_review_sentiments error for {url}: {error}")
        return {"sentiment": "neutral"}
