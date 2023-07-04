from django.shortcuts import render
import requests
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import redirect
import requests

# Create your views here.

# Salesforce Domain
DOMAIN = 'https://aidetic2-dev-ed.develop.my.salesforce.com'

# BaseURL after making it secure using ngrok
BASE_URL = 'https://34b5-171-76-81-105.ngrok-free.app'

''' Funtion for loading login page '''
def index(request):
    auth_endpoint = '/services/oauth2/authorize'
    REDIRECT_URI = f"{BASE_URL}/api/token"

    login_url = f"{DOMAIN}{auth_endpoint}?client_id={settings.CONSUMER_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    context = {
        'login_url' : login_url
    }
    return render(request, 'login.html', context)


''' Function for generating AccessToken '''
def get_access_token(request):
    code = request.GET.get('code')
    print(code, 'code')
    auth_endpoint = '/services/oauth2/token'
    REDIRECT_URI = f"{BASE_URL}/api/view-token"
    url = f"{DOMAIN}{auth_endpoint}"
    params = {
        'grant_type' : 'authorization_code',
        'client_id' : settings.CONSUMER_KEY,
        'client_secret' : settings.CONSUMER_SECRET,
        'redirect_uri' : REDIRECT_URI,
        'code' : code
    }
    response = requests.post(url=url, params=params)
    if response.status_code == 200:

        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        print(response.json())

        # Storing access token to file
        text_file = open("access_token.txt", "w")  
        text_file.write(access_token)
        text_file.close()

        # Storing refresh token to file
        text_file = open("refresh_token.txt", "w")  
        text_file.write(refresh_token)
        text_file.close()

        return HttpResponse(f'Your access Token is {access_token} and Refresh Token is {refresh_token}')
    return response.json()