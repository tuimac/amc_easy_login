from django.shortcuts import render
import boto3
import urllib3
import urllib
import json

# AWS Management console login process
def login(request):
    # Initialization 
    sts = boto3.client('sts')
    session_time = 12 * 60 * 60
    django_url = 'http://localhost:8000'

    # Get signin token
    credentials = sts.assume_role(
        RoleArn = 'arn:aws:iam::409826931222:role/AssumeRole',
        RoleSessionName = 'tuimac-admin'
    )['Credentials']

    urlCredentials = {
        'sessionId': credentials['AccessKeyId'],
        'sessionKey': credentials['SecretAccessKey'],
        'sessionToken': credentials['SessionToken']
    }

    url = f'https://signin.aws.amazon.com/federation?Action=getSigninToken&SessionDuration={session_time}&Session={urllib.parse.quote_plus(json.dumps(urlCredentials))}'

    http = urllib3.PoolManager()
    signin_token = json.loads(http.request('GET', url).data.decode())['SigninToken']

    # Create login url for AWS Management console
    url = f'https://ap-northeast-3.signin.aws.amazon.com/federation?Action=login&Issuer={urllib.parse.quote_plus(django_url)}&Destination={urllib.parse.quote_plus('https://console.aws.amazon.com/')}&SigninToken={urllib.parse.quote_plus(signin_token)}'
    print(url)

    # Pass the url to the frontend
    return render(request, 'login.html', {'url': url})