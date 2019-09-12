import json
from urllib.parse import urljoin

import requests

from upvest.config import API_VERSION
from upvest.exceptions import InvalidRequest


class Response:
    def __init__(self, result):
        self.status_code = result.status_code
        self.raw = result
        self.data = None
        if result.content:
            self.json = result.json()
            self.data = self.json.get("results", self.json)


# Request object
class Request:
    def __init__(self):
        pass

    def _check(self, value):
        if isinstance(value, int):
            pass
        elif isinstance(value, str):
            try:
                value.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError("Forbidden characters present, please remove")
        elif isinstance(value, dict):
            for val in value.values():
                self._check(val)
        elif isinstance(value, list):
            for val in value:
                self._check(val)
        else:
            raise ValueError("no valid JSON structure given")

    def _request(self, auth_instance, method, path, body=None):
        if body is not None:
            self._check(body)
            body = json.dumps(body)
        # Instantiate the respectively needed auth instance
        authenticated_headers = auth_instance.get_headers(method=method, path=path, body=body)
        authenticated_headers["User-Agent"] = auth_instance.user_agent
        # Execute request with authenticated headers
        request_url = urljoin(auth_instance.base_url, API_VERSION + path)
        response = requests.request(method, request_url, data=body, headers=authenticated_headers)
        if response.status_code >= 300:
            raise InvalidRequest(response)
        else:
            return response

    def post(self, **req_params):
        req_params["method"] = "POST"
        return self._request(**req_params)

    def get(self, **req_params):
        req_params["method"] = "GET"
        return self._request(**req_params)

    def patch(self, **req_params):
        req_params["method"] = "PATCH"
        return self._request(**req_params)

    def delete(self, **req_params):
        req_params["method"] = "DELETE"
        return self._request(**req_params)
