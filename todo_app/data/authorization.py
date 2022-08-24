from flask import redirect
from oauthlib.oauth2 import WebApplicationClient
from flask_login import UserMixin

import requests
import os

from todo_app.data.user import User

GITHUB_CLIENT_ID = 'aac58ee8eb7410822ff4'
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_ACCESS_URL = 'https://github.com/login/oauth/access_token'
TOKEN_URL = 'https://api.github.com/user'

def get_identity():
    client = WebApplicationClient(GITHUB_CLIENT_ID)
    redirect_github = client.prepare_request_uri(GITHUB_AUTHORIZE_URL);
    return redirect(redirect_github)

def get_user_details(code):
    client = WebApplicationClient(GITHUB_CLIENT_ID)

    token = client.prepare_token_request(GITHUB_ACCESS_URL, code = code)
    github_secret = os.environ.get('GITHUB_SECRET')
    headers = { 'Accept': 'application/json' }
    access_response = requests.post(token[0], headers = headers, data = token[2], auth = (GITHUB_CLIENT_ID, github_secret))
    
    access_token = access_response.json()['access_token']
    headers = { 'Authorization': 'Bearer %s' % access_token }
    user = requests.get(TOKEN_URL, headers = headers).json()

    return User(user['login'])
