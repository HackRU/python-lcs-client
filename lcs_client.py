'''
This is intended to be a serverside to help with hackru services that biggie back
on lcs login ang user data
'''

from datetime import datetime
from functools import wraps

import requests

LCS_URL_ROOT = 'https://api.hackru.org'
'''the url where lcs is'''

TESTING = True
'''weather or not to use test endpoint'''

def base_url():
    '''get the lcs base url'''
    if TESTING:
        return LCS_URL_ROOT + '/dev'
    else:
        return LCS_URL_ROOT + '/prod'

def get(endpoint, *args, **kwargs):
    '''does get request to lcs endpoint'''
    return requests.get(base_url() + endpoint, *args, **kwargs)

def post(endpoint, *args, **kwargs):
    '''does post request to lcs endpoint'''
    return requests.post(base_url() + endpoint, *args, **kwargs)

def pluck(_dict, *keys, defaults={}):
    '''
    util function. pluck keys from a dict and remove the rest
    if the key does not exist it will look into defaults.
    if there is no default it will throw a key error
    '''
    new = {}
    for key in keys:
        new[key] = _dict.get(key, defaults[key])


class ResponseError(Exception):
    '''error with an attached http Response'''
    def __init__(self, response):
        self.response = response
        if response.status_code == 200:
            self.status_code = response.json()['statusCode']
        else:
            self.status_code = response.status_code
            
    def __str__(self):
            return 'status: %d response: %s' % (self.status_code, self.response.json())

class InternalServerError(ResponseError):
    @staticmethod
    def check(response):        
        if response.status_code >= 500 or response.json().get('statusCode', 0) >= 500:
            raise InternalServerError(response)

class RequestError(ResponseError):
    '''ideally you shouldn't receve this. there was an issue with the input to the api'''
    @staticmethod
    def check(response):
        if response.status_code == 400 or response.json()['statusCode'] == 400:
            raise RequestError(response)

class CredentialError(RequestError):
    '''there was an issue login in with that credential, or a token is invalid'''
    @staticmethod
    def check(response):
        if response.status_code == 403 or response.json()['statusCode'] == 403:
            raise CredentialError(response)

def check_response(response):
    InternalServerError.check(response)
    RequestError.check(response)
    CredentialError.check(response)

login_hooks = []
def on_login(f):
    '''
    decorator. call the decorated function whenever we find a new user
    use case: get their profile and update local db.
    function should take in the user object as the first param
    '''
    login_hooks += f
    return f
    
_token_cache = {}
def validate_token(email, token):
    '''validates an lcs token and email pair'''
    #todo check cache first
    data = {'email': email, 'token': token}
    response = post('/validate', json=data)

    check_response(response)
    result = response.json()
    # todo check expiration
    # todo cache token and then call on_logins on cache insert
    return response.json()['body']

def login(email, password):
    '''gets a token for a user'''
    data = {'email': email, 'password': password}
    response = post('/authorize', json=data)
    
    check_response(response)
    result = response.json()
    #todo cache insert and call get profile to call on_logins
    return result['body']['auth']

def get_profile(email, token, auth_email=None):
    '''
    gets the profile of a user. add auth_email if you are looking at the users profile
    from a different account
    '''
    if not auth_email:
        auth_email = email

    data = {'email': email, 'token': token, 'auth_email': auth_email,
            'query': {'email': email}}
    response = post('/read', json=data)

    check_response(response)
    return response.json()['body'][0]

def get_dm_for(email, token, other_user):
    '''get a dm link to talk with another user on slack'''
    raise Exception('not yet implemented')

class User:
    '''a user object to easily call other endpoints on behalf of a user'''
    def __init__(self, email, password=None, token=None):
        '''log the user and get a handle. requires'''
        if not password and not token:
            raise Exception('must provide token or password to login')

        self.email = email
        if password:
            full_token = login(email, password)
            self.token = full_token['token']

        if token:
            validate_token(email, token)
            self.token = token

    def profile(self):
        '''call lcs to get the user's profile'''
        return get_profile(self.email, self.token)

    def dm_link_for(other_user):
        '''get a dm link for another user's slack'''
        return get_dm_for(self.email, self.token, other_user)
