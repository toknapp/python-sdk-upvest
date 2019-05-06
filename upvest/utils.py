import json
import requests
import re

from upvest.config import API_VERSION
from upvest.config import BASE_URL

from upvest.exceptions import NoPreviousPage, NoNextPage

# Response Objects, with and without pagination
class Response(object):
    def __init__(self, result, **req_params):
        self.status_code = result.status_code
        self.req_params = req_params
        self.raw = result
        try:
            self.json = result.json()
            try:
                self.data = self.json['results']
            except:
                self.data = self.json
        except:
            #raise ValueError
            self.data = None

class PaginatedResponse(Response):
    def __init__(self, result, **req_params):
        Response.__init__(self, result, **req_params)

    def previous(self):
        link = self.json['previous']
        if link == None:
            raise NoPreviousPage('There is no previous page')
        self.req_params['path'] = link.split(API_VERSION)[-1]
        return Request().get(**self.req_params)
        
    def next(self):
        link = self.json['next']
        if link == None:
            raise NoNextPage('There is no next page')
        self.req_params['path'] = link.split(API_VERSION)[-1]
        return Request().get(**self.req_params)

# Request object
class Request(object):
    def __init__(self):
        pass

    def _request(self, **req_params):
        # Set request parameters
        response_instance = req_params.get('response_instance', Response)
        body = req_params.get('body', None)
        path = req_params.get('path')
        method = req_params.get('method')
        if body is not None:
            for value in body.values():
                try:
                    value.encode('ascii')
                except UnicodeEncodeError:
                    raise Exception('Forbidden characters present, please remove')
        # Instantiate the respectively needed auth instance
        auth_instance = req_params.get('auth_instance')
        authenticated_headers = auth_instance.get_headers(**req_params)
        # Execute request with authenticated headers
        request_url = BASE_URL + API_VERSION + path
        return response_instance(requests.request(method, request_url, json=body, headers=authenticated_headers), **req_params)

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