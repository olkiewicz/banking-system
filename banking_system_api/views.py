from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_system_api.models import BankAccount
from banking_system_api.serializers import BankAccountSerializer


class BankAccountListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the bank accounts
        '''
        bank_accounts = BankAccount.objects.all()
        # bank_accounts = BankAccount.objects.filter(client=request.data.get('client'))
        # bank_accounts = BankAccount.objects.filter(client=request.client.id)
        serializer = BankAccountSerializer(bank_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the bank account with given data
        '''
        data = {
            'balance': 0.00,
            'client': request.data.get('client'),
            'currency': request.data.get('currency'),
            'type_of_account': 'regular account'
        }
        serializer = BankAccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
