from django.shortcuts import render
import boto3
import urllib3
import urllib
import json

# AWS Management console login process
def login(request):
    # Initialization 
    sts = boto3.client('sts')
    session_time = 24 * 60 * 60
    django_url = 'http://localhost:8000'

    # Get signin token
    credentials = sts.get_federation_token(
        Name = 'tuimac-admin',
        PolicyArns = [{ 'arn': 'arn:aws:iam::aws:policy/AdministratorAccess' }],
        DurationSeconds = session_time
    )['Credentials']

    urlCredentials = {
        'sessionId': credentials['AccessKeyId'],
        'sessionKey': credentials['SecretAccessKey'],
        'sessionToken': credentials['SessionToken']
    }

    url = f'https://signin.aws.amazon.com/federation?Action=getSigninToken&&Session={urllib.parse.quote_plus(json.dumps(urlCredentials))}'

    http = urllib3.PoolManager()
    signin_token = json.loads(http.request('GET', url).data.decode())['SigninToken']

    # Create login url for AWS Management console
    url = f'https://signin.aws.amazon.com/federation?Action=login&Issuer={urllib.parse.quote_plus(django_url)}&Destination={urllib.parse.quote_plus('https://console.aws.amazon.com/')}&SigninToken={urllib.parse.quote_plus(signin_token)}'

    # Pass the url to the frontend
    return render(request, 'login.html', {'url': url})