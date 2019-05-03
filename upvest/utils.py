import json
import requests
import re

from upvest.config import API_VERSION
from upvest.config import BASE_URL

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

    def previous(self, **req_params):
        link = self.json['previous']
        self.req_params['path'] = link.split(link, API_VERSION)[-1]
        return Response(Request().get(**self.req_params))

    def next(self, **req_params):
        link = self.json()['next']
        self.req_params['path'] = link.split(link, API_VERSION)[-1]
        return Response(Request().get(**self.req_params))

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

class User(object):
    def __init__(self, auth_instance):
        self.path = '/tenancy/users/'
        self.auth_instance = auth_instance

    def create(self, username, password):
        # Set username and password for the user
        body = {
            'username': username,
            'password': password,
        }
        return Request().post(auth_instance=self.auth_instance, path=self.path, body=body)

    def retrieve(self, username):
        # Retrieve single user
        return Request().get(auth_instance=self.auth_instance, path=self.path + username)

    def list(self):
        # Retrieve user list
        return Request().get(auth_instance=self.auth_instance, path=self.path, response_instance=PaginatedResponse)

    def update(self, username, current_password, new_password):
        # Provide current and new password
        body = {
            'old_password': current_password,
            'new_password': new_password,
        }
        return Request().patch(auth_instance=self.auth_instance, path=self.path + username, body=body)

    def delete(self, username):
        # Deregister a user
        return Request().delete(auth_instance=self.auth_instance, path=self.path + username)


class Asset(object):
    def __init__(self, auth_instance):
        self.path = '/assets/'
        self.auth_instance = auth_instance

    def list(self):
        return Request().get(auth_instance=self.auth_instance, path=self.path, response_instance=PaginatedResponse)


class Wallet(object):
    def __init__(self, auth_instance):
        self.path = '/kms/wallets/'
        self.auth_instance = auth_instance

    def list(self):
        # Retrieve list of all wallets for a user
        return Request().get(auth_instance=self.auth_instance, path=self.path, response_instance=PaginatedResponse)

    def retrieve(self, wallet_id):
        # Retrieve specific wallet for a user
        return Request().get(auth_instance=self.auth_instance, path=self.path + wallet_id)

    def create(self, asset_id):
        # Get desired asset id from assets list
        # Provide password and asset_id for wallet creation
        body = {
            'password': self.auth_instance.password,
            'asset_id': asset_id,
        }
        return Request().post(auth_instance=self.auth_instance, path=self.path, body=body)


class Transaction(object):
    def __init__(self, auth_instance):
        self.path = '/tx/'
        self.auth_instance = auth_instance

    def send(self, wallet_id, asset_id, quantity, fee, recipient):
        # Provide password and asset_id for wallet creation
        body = {
            'password': self.auth_instance.password,
            'wallet_id': wallet_id,
            'asset_id': asset_id,
            'quantity': quantity,
            'fee': fee,
            'recipient': recipient,
        }
        response = Request().post(auth_instance=self.auth_instance, path=self.path, body=body)
        return response

    def retrieve(self, txhash):
        # Define tx endpoint
        return Request().post(auth_instance=self.auth_instance, path=self.path + txhash)
