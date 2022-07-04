import logging

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_system_api.models import BankAccount, Address, Client
from banking_system_api.serializers import BankAccountSerializer, AddressSerializer, ClientSerializer


class BankAccountListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, client_id=None):
        '''
        List all the bank accounts or bank accounts for given client
        '''

        if client_id:
            bank_accounts = BankAccount.objects.filter(client_id=client_id)

        else:
            bank_accounts = BankAccount.objects.all()

        serializer = BankAccountSerializer(bank_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the bank account with given data
        '''
        data = {
            'balance': 0.00,
            'client_id': request.data.get('client_id'),
            'currency': request.data.get('currency'),
            'type_of_account': 'regular account'
        }
        serializer = BankAccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # 3. Delete
    # def delete(self, request, *args, **kwargs):
    #     '''
    #     Delete the bank
    #     '''


class AddressListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

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


class ClientsListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

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
        print(f'----{data}')
        serializer = ClientSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
