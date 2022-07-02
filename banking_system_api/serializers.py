from rest_framework import serializers

from banking_system_api.models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['balance', 'client', 'currency', 'type_of_account', 'creation_date']
