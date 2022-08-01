import requests


class CsrfRequest:
    def __init__(self, login_url, username, password):
        self.login_url = login_url
        self.username = username
        self.password = password
        self.session_id = ''
        self.csrf_token = ''

    def request(self, method, url, data=None, token_headers=None):
        if token_headers is None:
            token_headers = {}

        if not self.session_id:
            self.authenticate()

        cookies = {
            'csrftoken': self.csrf_token,
            'sessionid': self.session_id
        }

        if method in ['POST', 'DELETE', 'PATCH']:
            token_headers['X-CSRFToken'] = self.csrf_token

        return requests.request(method, url, data=data, headers=token_headers, cookies=cookies)

    def authenticate(self):
        response = requests.get(self.login_url)

        if response.status_code != 200:
            raise Exception

        self.csrf_token = response.cookies.get('csrftoken')
        data = {
            'username': self.username,
            'password': self.password,
            'csrfmiddlewaretoken': self.csrf_token
        }
        cookies = {
            'csrftoken': self.csrf_token
        }

        response = requests.post(self.login_url, data, cookies=cookies, allow_redirects=False)

        self.session_id = response.cookies.get('sessionid')
        self.csrf_token = response.cookies.get('csrftoken')


authenticated_request = CsrfRequest('http://127.0.0.1:8000/api-auth/login/', 'admin', '123')
transfers_response = authenticated_request.request('GET',
    'http://127.0.0.1:8000/api/accounts/'
)

print()
print(f'{transfers_response.status_code}')
print(f'{transfers_response.text}')


request_data = {'balance': '999999.13'}
patch_request = authenticated_request.request('PATCH',
'http://127.0.0.1:8000/api/accounts/1',
                                              data=request_data
                                              )
# request_data = {'name': 'test account type'}
# transfers_response = authenticated_request.request('POST',
#     'http://127.0.0.1:8000/api/account_types/',
#     data=request_data
# )
#
print()
print(f'{patch_request.status_code}')
print(f'{patch_request.text}')
print(f'{patch_request.headers}')


transfers_response = authenticated_request.request('GET',
    'http://127.0.0.1:8000/api/accounts/'
)

print()
print(f'{transfers_response.status_code}')
print(f'{transfers_response.text}')
