from django.http import Http404
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from banking_system_api.models import Account, Address, Client, AccountType, Currency, Transfer
from banking_system_api.serializers import AccountSerializer, AddressSerializer, ClientSerializer, \
    AccountTypeSerializer, CurrencySerializer, TransferSerializer


class BaseApiView(GenericAPIView):
    pagination_class = PageNumberPagination

    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]


class AddressApiView(BaseApiView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        address_id = kwargs.get('address_id')

        if address_id:
            data = self.get_queryset().filter(id=address_id)

        else:
            data = self.get_queryset()

        serializer = self.get_serializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'full_address': request.data.get('full_address')
        }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        address_id = kwargs.get('address_id')
        address = self.get_queryset().get(id=address_id)
        address.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientsListApiView(BaseApiView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'address_id': request.data.get('address_id')
        }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')

        try:
            client = self.get_queryset().get(id=client_id)
            client.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Client.DoesNotExist:
            raise Http404


class AccountTypeApiView(BaseApiView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name')
        }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        account_type_id = kwargs.get('account_type_id')

        try:
            account_type = self.get_queryset().get(id=account_type_id)
            account_type.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except AccountType.DoesNotExist:
            raise Http404


class CurrencyApiView(BaseApiView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = {
            'symbol': request.data.get('symbol'),
            'name': request.data.get('name')
        }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,  *args, **kwargs):
        currency_id = kwargs.get('currency_id')

        try:
            currency = self.queryset.get(id=currency_id)
            currency.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Currency.DoesNotExist:
            raise Http404


class AccountApiView(BaseApiView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @staticmethod
    def generate_account_number():
        # FIXME
        return '12345678901234567890123456'

    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')

        if account_id:
            try:
                data = self.get_queryset().get(id=account_id)
                serializer = self.get_serializer(data)

            except Account.DoesNotExist:
                raise Http404

        else:
            data = self.get_queryset()
            serializer = self.get_serializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'account_number': self.generate_account_number(),
            'balance': request.data.get('balance'),
            'client_id': request.data.get('client_id'),
            'currency_id': request.data.get('currency_id'),
            'account_type_id': request.data.get('account_type_id')
        }

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        account = self.get_queryset().get(id=account_id)
        account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        account = self.get_queryset().get(id=account_id)
        serializer = self.get_serializer(account, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class TransferApiView(BaseApiView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'sender_account_id': request.data.get('sender_account_id'),
            'recipient_account_id': request.data.get('recipient_account_id'),
            'recipient_details': request.data.get('recipient_details'),
            'amount': request.data.get('amount')
        }

        if 'is_external' in request.data.keys():
            data.update({'is_external': True})

        if 'title' in request.data.keys():
            data.update({'title': request.data.get("title")})

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        transfer_id = kwargs.get('transfer_id')
        transfer = self.get_queryset().get(id=transfer_id)
        transfer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        transfer_id = kwargs.get('transfer_id')

        try:
            transfer = self.get_queryset().get(id=transfer_id)
            serializer = self.get_serializer(transfer, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                return Response(status=status.HTTP_204_NO_CONTENT)

        except Account.DoesNotExist:
            raise Http404
