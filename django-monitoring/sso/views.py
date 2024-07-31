import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import login, get_user_model, logout

# View to render Login Page
def login_view(request):
    return render(request, 'login.html')


# Redirects user to Github Auth
def github_login(request):
    host = request.get_host()
    redirect_uri = f'http://{host}/login/callback/'
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id={settings.CLIENT_ID}&redirect_uri={redirect_uri}&scope=use'

    return redirect(github_auth_url)


# GitHub Auth Callback, logs in user if valid.
def github_callback(request):
    # Get the code from the request query params
    code = request.GET.get('code')

    # Get the access token from GitHub using oauth
    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': code,
    }
    headers = {'Accept': 'application/json'}
    token_response = requests.post(token_url, data=token_data, headers=headers)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    # Get user info from GitHub
    user_info_url = 'https://api.github.com/user'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'token {access_token}'})
    user_info = user_info_response.json()

    # If user info does not contain login, return invalid request
    if 'login' not in user_info:
        return render(request, 'invalid_request.html')

    # Get or create user and login
    user, _ = get_user_model().objects.get_or_create(username=user_info['login'])
    login(request, user)

    return redirect('/')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('/login/')
