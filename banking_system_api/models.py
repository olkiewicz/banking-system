from django.db import models


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    full_address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.full_address}'

    class Meta:
        ordering = ['id']


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['id']


class AccountType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(max_length=26)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account_type_id = models.ForeignKey(AccountType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account_number}: {self.balance} {self.currency_id}'

    class Meta:
        ordering = ['creation_date']


class Transfer(models.Model):
    id = models.AutoField(primary_key=True)
    transfer_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    sender_account_id = models.ForeignKey(Account, related_name='sender', on_delete=models.CASCADE)
    recipient_account_id = models.ForeignKey(Account, related_name='recipient', on_delete=models.CASCADE, null=True)
    recipient_details = models.CharField(max_length=200, default='')
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    title = models.CharField(max_length=200, default='')
    is_external = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        ordering = ['transfer_date']
