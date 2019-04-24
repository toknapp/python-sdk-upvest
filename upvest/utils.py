import json
import requests

from upvest.config import API_VERSION
from upvest.config import BASE_URL

class ResultObj(result, **req_params):
    def __init__(self):
        self.status_code = result.status_code
        try:
            self.json = result.json()
        except:
            #raise ValueError
            pass

    def data(self):
        try:
            self.data = json.loads(self.json())['results']
        except:
            self.data = json.loads(self.json())
        return self.data

    def previous(self,**req_params):
        link = json.loads(self.json())['previous']
        return ResultObj(Request().get(link,**req_params))

    def next(self,**req_params):
        link = json.loads(self.json())['next']
        return ResultObj(Request().get(link,**req_params))

        

class Request(object):
    def __init__(self):
        pass

    def _request(self, **req_params):
        # Set request parameters
        body = req_params.get('body', None)
        path = req_params.get('path')
        method = req_params.get('method')
        # Instantiate the respectively needed auth instance
        auth_instance = req_params.get('auth_instance')
        authenticated_headers = auth_instance.get_headers(**req_params)
        # Execute request with authenticated headers
        request_url = BASE_URL + API_VERSION + path
        return requests.request(method, request_url, json=body, headers=authenticated_headers) 
        
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
