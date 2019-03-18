# coding: utf-8
import requests
from requests.exceptions import RequestException


def get_requests(scheme, host, endpoint, token):
    try:
        url = scheme + "://" + host + endpoint
        if token == "":
            response = requests.get(url)
        else:
            headers = {"Authorization": token}
            response = requests.get(url, headers=headers)
        response.raise_for_status()
        d_response = response.json()
    except RequestException:
        return None

    return d_response


def post_requests_no_data(scheme, host, endpoint, token):
    try:
        url = scheme + "://" + host + endpoint
        if token == "":
            response = requests.post(url)
        else:
            headers = {"Authorization": token}
            response = requests.post(url, headers=headers)
        response.raise_for_status()
        d_response = response.json()
    except RequestException:
        return None

    return d_response
