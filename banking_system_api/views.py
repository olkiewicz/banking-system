from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_system_api.models import Account, Address, Client, AccountType, Currency
from banking_system_api.serializers import AccountSerializer, AddressSerializer, ClientSerializer, \
    AccountTypeSerializer, CurrencySerializer


class BaseApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]


class AddressApiView(BaseApiView):
    @staticmethod
    def get_object(pk):
        try:
            return Address.objects.get(id=pk)

        except Address.DoesNotExist:
            raise Http404

    def get(self, request, address_id=None):
        if address_id:
            addresses = Address.objects.filter(id=address_id)

        else:
            addresses = Address.objects.all()

        serializer = AddressSerializer(addresses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, address_id=None):
        data = {
            'full_address': request.data.get('full_address')
        }
        serializer = AddressSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id):
        address = self.get_object(address_id)
        address.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientsListApiView(BaseApiView):
    def get(self, request, client_id=None):
        addresses = Client.objects.all()
        serializer = ClientSerializer(addresses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, client_id=None):
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

    def delete(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            client.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Client.DoesNotExist:
            raise Http404


class AccountTypeApiView(BaseApiView):
    def get(self, request, account_type_id=None):
        account_types = AccountType.objects.all()
        serializer = AccountTypeSerializer(account_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, account_type_id=None):
        data = {
            'name': request.data.get('name')
        }
        serializer = AccountTypeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, account_type_id=None):
        try:
            account_type = AccountType.objects.get(id=account_type_id)
            account_type.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except AccountType.DoesNotExist:
            raise Http404


class CurrencyApiView(BaseApiView):
    def get(self, request, currency_id=None):
        account_types = Currency.objects.all()
        serializer = CurrencySerializer(account_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, currency_id=None):
        data = {
            'symbol': request.data.get('symbol'),
            'name': request.data.get('name')
        }
        serializer = CurrencySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, currency_id):
        try:
            currency = Currency.objects.get(id=currency_id)
            currency.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Currency.DoesNotExist:
            raise Http404


class AccountApiView(BaseApiView):
    @staticmethod
    def get_object(account_id):
        try:
            return Account.objects.get(id=account_id)

        except Account.DoesNotExist:
            raise Http404

    @staticmethod
    def generate_account_number():
        # FIXME
        return '12345678901234567890123456'

    def get(self, request, account_id=None):
        if account_id:
            data = self.get_object(account_id)
            serializer = AccountSerializer(data)

        else:
            data = Account.objects.all()
            serializer = AccountSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, account_id=None):
        data = {
            'account_number': self.generate_account_number(),
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

    def delete(self, request, account_id):
        account = self.get_object(account_id)
        account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, account_id):
        account = self.get_object(account_id)
        serializer = AccountSerializer(account, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
