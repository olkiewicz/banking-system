from rest_framework import serializers

from banking_system_api.models import Account, Address, Client, AccountType, Currency, Transfer


class AccountSerializer(serializers.ModelSerializer):
    outgoing_transfers = serializers.StringRelatedField(many=True, required=False)
    incoming_transfers = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Account
        fields = ['id', 'account_number', 'balance', 'outgoing_transfers', 'incoming_transfers', 'client_id', 'currency_id', 'account_type_id', 'creation_date']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'full_address']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'address_id']


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'name']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'symbol', 'name']


class TransferSerializer(serializers.ModelSerializer):
    transfer_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Transfer
        model = Transfer
        fields = ['id', 'transfer_date', 'sender_account_id', 'recipient_account_id', 'recipient_details', 'amount',
                  'currency_id', 'title', 'is_external']
