import json
import requests
import re

from upvest.config import API_VERSION
from upvest.config import BASE_URL

class Response(object):
    def __init__(self, result, **req_params):
        self.status_code = result.status_code
        self.response_data = None
        self.req_params = req_params
        try:
            self.json = result.json()
        except:
            #raise ValueError
            pass

    def data(self):
        try:
            self.response_data = self.json['results']
        except:
            self.response_data = self.json
        return self.response_data

    def previous(self,**req_params):
        link = self.json['previous']
        self.req_params['path'] = link.split(link, API_VERSION)[-1]
        return Response(Request().get(**self.req_params))

    def next(self,**req_params):
        link = self.json()['next']
        self.req_params['path'] = link.split(link, API_VERSION)[-1]
        return Response(Request().get(**self.req_params))


class Request(object):
    def __init__(self):
        pass

    def _request(self, **req_params):
        # Set request parameters
        regex = re.compile('\\')
        body = req_params.get('body', None)
        path = req_params.get('path')
        method = req_params.get('method')
        for key in body.keys():
            if (regex.search(body['key']) != None):
                raise Exception('forbidden characters are present')
        # Instantiate the respectively needed auth instance
        auth_instance = req_params.get('auth_instance')
        authenticated_headers = auth_instance.get_headers(**req_params)
        # Execute request with authenticated headers
        request_url = BASE_URL + API_VERSION + path
        return Response(requests.request(method, request_url, json=body, headers=authenticated_headers), **req_params)

    def post(self, **req_params):
        req_params['method'] = 'POST'
        return self._request(**req_params)
    
    def get(self, **req_params):
        req_params['method'] = 'GET'
        return self._request(**req_params)
    
    def patch(self, **req_params):
        req_params['method'] = 'PATCH'
        return self._request(**req_params)
    
    def delete(self, **req_params):
        req_params['method'] = 'DELETE'
        return self._request(**req_params)
