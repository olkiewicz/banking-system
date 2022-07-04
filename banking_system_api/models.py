from django.db import models


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    full_address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.full_address}'


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    currency = models.CharField(max_length=20)
    type_of_account = models.CharField(max_length=50)  # FIXME: use foreignkey
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.balance} {self.currency}'

