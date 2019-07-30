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

    def _request(self, **req_params):
        # Set request parameters
        body = req_params.get("body", None)
        path = req_params.get("path")
        method = req_params.get("method")
        if body is not None and body != {}:
            for value in body.values():
                if isinstance(value, int):
                    pass
                else:
                    try:
                        value.encode("ascii")
                    except UnicodeEncodeError:
                        raise Exception("Forbidden characters present, please remove")
        # Instantiate the respectively needed auth instance
        auth_instance = req_params.get("auth_instance")
        authenticated_headers = auth_instance.get_headers(method=method, path=path, body=body)
        # Execute request with authenticated headers
        request_url = urljoin(auth_instance.base_url, API_VERSION + path)
        response = requests.request(method, request_url, json=body, headers=authenticated_headers)
        if response.status_code >= 300:
            raise InvalidRequest(response.text)
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
