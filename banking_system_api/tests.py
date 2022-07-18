from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.test import Client


API_ADDRESSES_URL = '/api/addresses/'
API_CURRENCIES_URL = '/api/currencies/'
API_ACCOUNT_TYPES_URL = '/api/account_types/'
API_CLIENTS_URL = '/api/clients/'
API_ACCOUNT_URL = '/api/accounts/'


def get_first_address_json():
    return {
        'full_address': 'Berlin, Rommel 213'
    }


def get_second_address_json():
    return {
        'full_address': 'London, Oxford 32A'
    }


def get_first_client_json(address_id):
    return {
        'first_name': 'Alexander',
        'last_name': 'Winner',
        'address_id': address_id
    }


def get_second_client_json(address_id):
    return {
        'first_name': 'John',
        'last_name': 'Smith',
        'address_id': address_id
    }


def get_first_account_type_json():
    return {
        'name':  'checking account'
    }


def get_second_account_type_json():
    return {
        'name': 'savings account'
    }


def get_first_currency_json():
    return {
        'symbol': 'USD',
        'name': 'American dollar'
    }


def get_second_currency_json():
    return {
        'symbol': 'AUD',
        'name': 'Australian dollar'
    }


def get_first_account_json(client_id, currency_id, account_type_id):
    return {
        'account_number': '61 1090 1014 0000 0712 1981 2874',
        'balance': 2136.99,
        'client_id': client_id,
        'currency_id': currency_id,
        'account_type_id': account_type_id,
    }


def get_second_account_json(client_id, currency_id, account_type_id):
    return {
        'account_number': '44 1090 1111 0000 0712 1981 1234',
        'balance': 15000123.00,
        'client_id': client_id,
        'currency_id': currency_id,
        'account_type_id': account_type_id,
    }


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@email.com', password='123')
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION=f'Token {token.key}')

    def create_address_and_get_its_id(self, address_json) -> int:
        response = self.client.post(API_ADDRESSES_URL, address_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response.data.get('id')

    def create_client_and_get_its_id(self, client_json) -> int:
        response = self.client.post(API_CLIENTS_URL, client_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response.data.get('id')

    def create_account_type_and_get_its_id(self, account_type_json):
        response = self.client.post(API_ACCOUNT_TYPES_URL, account_type_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response.data.get('id')

    def create_currency_and_get_its_id(self, currency_json):
        response = self.client.post(API_CURRENCIES_URL, currency_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response.data.get('id')

    def create_account_and_get_its_id(self, account_json):
        response = self.client.post(API_ACCOUNT_URL, account_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response.data.get('id')


class AddressesTestCase(BaseTestCase):
    def test_post_address(self):
        self.create_address_and_get_its_id(get_first_address_json())

    def test_get_addresses(self):
        first_address_id = self.create_address_and_get_its_id(get_first_address_json())
        second_address_id = self.create_address_and_get_its_id(get_second_address_json())

        response = self.client.get(API_ADDRESSES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue([result.get('id') in (first_address_id, second_address_id) for result in response.data])

    def test_delete_address(self):
        first_address_id = self.create_address_and_get_its_id(get_first_address_json())
        second_address_id = self.create_address_and_get_its_id(get_second_address_json())

        response = self.client.delete(f'{API_ADDRESSES_URL}{first_address_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(API_ADDRESSES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue([result.get('id') == second_address_id for result in response.data])


class ClientsTestCase(BaseTestCase):
    def test_post_client(self):
        address_id = self.create_address_and_get_its_id(get_first_address_json())
        self.create_client_and_get_its_id(get_first_client_json(address_id))

    def test_get_clients(self):
        first_address_id = self.create_address_and_get_its_id(get_first_address_json())
        second_address_id = self.create_address_and_get_its_id(get_second_address_json())

        first_client_id = self.create_client_and_get_its_id(get_first_client_json(first_address_id))
        second_client_id = self.create_client_and_get_its_id(get_second_client_json(second_address_id))

        response = self.client.get(API_CLIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue([result.get('id') in (first_client_id, second_client_id) for result in response.data])

    def test_delete_client(self):
        first_address_id = self.create_address_and_get_its_id(get_first_address_json())
        second_address_id = self.create_address_and_get_its_id(get_second_address_json())

        first_client_id = self.create_client_and_get_its_id(get_first_client_json(first_address_id))
        second_client_id = self.create_client_and_get_its_id(get_second_client_json(second_address_id))

        response = self.client.delete(f'{API_CLIENTS_URL}{first_client_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(API_CLIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue([result.get('id') == second_client_id for result in response.data])


class AccountTypesTestCase(BaseTestCase):
    def test_post_account_type(self):
        self.create_account_type_and_get_its_id(get_first_account_type_json())

    def test_get_account_types(self):
        first_account_type_id = self.create_account_type_and_get_its_id(get_first_account_type_json())
        second_account_type_id = self.create_account_type_and_get_its_id(get_second_account_type_json())

        response = self.client.get(API_ACCOUNT_TYPES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue([result.get('id') in (first_account_type_id, second_account_type_id) for result in response.data])

    def test_delete_account_type(self):
        first_account_type_id = self.create_account_type_and_get_its_id(get_first_account_type_json())
        second_account_type_id = self.create_account_type_and_get_its_id(get_second_account_type_json())

        response = self.client.delete(f'{API_ACCOUNT_TYPES_URL}{first_account_type_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(API_ACCOUNT_TYPES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue([result.get('id') == second_account_type_id for result in response.data])


class CurrenciesTestCase(BaseTestCase):
    def test_post_currency(self):
        self.create_currency_and_get_its_id(get_first_currency_json())

    # specific case caused of pagination
    def test_get_currencies(self):
        first_currency_id = self.create_currency_and_get_its_id(get_first_currency_json())
        second_currency_id = self.create_currency_and_get_its_id(get_second_currency_json())

        response = self.client.get(API_CURRENCIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)
        self.assertTrue([result.get('id') in (first_currency_id, second_currency_id) for result in response.data.get('results')])

    def test_delete_currency(self):
        first_currency_id = self.create_currency_and_get_its_id(get_first_currency_json())
        second_currency_id = self.create_currency_and_get_its_id(get_second_currency_json())

        response = self.client.delete(f'{API_CURRENCIES_URL}{first_currency_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(API_CURRENCIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertTrue([result.get('id') == second_currency_id for result in response.data.get('results')])


class AccountsTestCase(BaseTestCase):
    def test_post_account(self):
        address_id = self.create_address_and_get_its_id(get_first_address_json())
        client_id = self.create_client_and_get_its_id(get_first_client_json(address_id))
        currency_id = self.create_currency_and_get_its_id(get_first_currency_json())
        account_type_id = self.create_account_type_and_get_its_id(get_first_account_type_json())

        self.create_account_and_get_its_id(get_first_account_json(client_id, currency_id, account_type_id))

    def test_get_accounts(self):
        first_address_id = self.create_address_and_get_its_id(get_first_address_json())
        first_client_id = self.create_client_and_get_its_id(get_first_client_json(first_address_id))
        first_currency_id = self.create_currency_and_get_its_id(get_first_currency_json())
        first_account_type_id = self.create_account_type_and_get_its_id(get_first_account_type_json())
        first_account_id = self.create_account_and_get_its_id(get_first_account_json(first_client_id, first_currency_id, first_account_type_id))

        second_address_id = self.create_address_and_get_its_id(get_second_address_json())
        second_client_id = self.create_client_and_get_its_id(get_second_client_json(second_address_id))
        second_currency_id = self.create_currency_and_get_its_id(get_second_currency_json())
        second_account_type_id = self.create_account_type_and_get_its_id(get_second_account_type_json())
        second_account_id = self.create_account_and_get_its_id(get_first_account_json(second_client_id, second_currency_id, second_account_type_id))

        response = self.client.get(API_ACCOUNT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue([result.get('id') in (first_account_id, second_account_id) for result in response.data])

    def test_delete_currency(self):
        first_address_id = self.create_address_and_get_its_id(get_first_address_json())
        first_client_id = self.create_client_and_get_its_id(get_first_client_json(first_address_id))
        first_currency_id = self.create_currency_and_get_its_id(get_first_currency_json())
        first_account_type_id = self.create_account_type_and_get_its_id(get_first_account_type_json())
        first_account_id = self.create_account_and_get_its_id(get_first_account_json(first_client_id, first_currency_id, first_account_type_id))

        second_address_id = self.create_address_and_get_its_id(get_second_address_json())
        second_client_id = self.create_client_and_get_its_id(get_second_client_json(second_address_id))
        second_currency_id = self.create_currency_and_get_its_id(get_second_currency_json())
        second_account_type_id = self.create_account_type_and_get_its_id(get_second_account_type_json())
        second_account_id = self.create_account_and_get_its_id(get_first_account_json(second_client_id, second_currency_id, second_account_type_id))

        response = self.client.delete(f'{API_ACCOUNT_URL}{second_account_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(API_ACCOUNT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue([result.get('id') == first_account_id for result in response.data])
