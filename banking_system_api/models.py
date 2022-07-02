from django.db import models


class BankAccount(models.Model):
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    client = models.IntegerField()
    currency = models.CharField(max_length=20)
    type_of_account = models.CharField(max_length=50)  # FIXME: use foreignkey
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.balance} {self.currency}'
