from flask import redirect
from oauthlib.oauth2 import WebApplicationClient

GITHUB_CLIENT_ID = 'aac58ee8eb7410822ff4'
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
REDIRECT_URL = 'http://localhost:5000/login/callback'

def get_identity():
    client = WebApplicationClient(GITHUB_CLIENT_ID)
    redirect_github = client.prepare_request_uri(GITHUB_AUTHORIZE_URL);
    return redirect(redirect_github)
