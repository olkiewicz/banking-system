import logging

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_system_api.models import Account, Address, Client, AccountType, Currency
from banking_system_api.serializers import AccountSerializer, AddressSerializer, ClientSerializer, \
    AccountTypeSerializer, CurrencySerializer


class BaseApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]


class AddressListApiView(BaseApiView):
    # 1. Get all
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request):
        data = {
            'full_address': request.data.get('full_address')
        }
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientsListApiView(BaseApiView):
    # 1. Get all
    def get(self, request):
        addresses = Client.objects.all()
        serializer = ClientSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'address_id': request.data.get('address_id')
        }
        serializer = ClientSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountTypeApiView(BaseApiView):
    # 1. Get all
    def get(self, request):
        account_types = AccountType.objects.all()
        serializer = AccountTypeSerializer(account_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request):
        data = {
            'name': request.data.get('name')
        }
        serializer = AccountTypeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyApiView(BaseApiView):
    # 1. Get all
    def get(self, request):
        account_types = Currency.objects.all()
        serializer = CurrencySerializer(account_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request):
        data = {
            'symbol': request.data.get('symbol'),
            'name': request.data.get('name')
        }
        serializer = CurrencySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_account_number():
    # FIXME
    return '12345678901234567890123456'


class AccountListApiView(BaseApiView):
    # 1. List all
    def get(self, request, client_id=None):
        '''
        List all the bank accounts or bank accounts for given client
        '''

        if client_id:
            accounts = Account.objects.filter(client_id=client_id)

        else:
            accounts = Account.objects.all()

        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request):
        '''
        Create the bank account with given data
        '''
        # FIXME: use client's name
        data = {
            'account_number': generate_account_number(),
            'balance': request.data.get('balance'),
            'client_id': request.data.get('client_id'),
            'currency_id': request.data.get('currency_id'),
            'account_type_id': request.data.get('account_type_id')
        }

        serializer = AccountSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


