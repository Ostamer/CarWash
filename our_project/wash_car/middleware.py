import requests
from django.http import JsonResponse


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            username, token_access = self.get_info_from_request(request)
            if not username or not token_access:
                return self.unauthorized_response()
            if not self.verify_token(username, token_access):
                return self.unauthorized_response()

        response = self.get_response(request)
        return response

    def get_info_from_request(self, request):
        username = request.headers.get('Username')
        authorization_header = request.headers.get('Authorization')
        token_access = ""
        if authorization_header.startswith('Bearer '):
            token_access = authorization_header.split(' ')[1]
        return username, token_access

    def verify_token(self, username, token_access):
        api_url = 'http://127.0.0.1:8000/auth/token/check'
        payload = {
            'username': username,
            'access_token': token_access
        }
        try:
            response = requests.post(api_url, json=payload)
            print(response.status_code)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException:
            return False

    def unauthorized_response(self):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
