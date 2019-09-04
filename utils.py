import requests

def get_request_json(url):
    r = requests.get(url)
    r = r.json()

    return r
