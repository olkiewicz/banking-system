from django.urls import path, include
from .views import (
    BankAccountListApiView, AddressListApiView, ClientsListApiView, AccountTypeApiView, CurrencyApiView,
)

urlpatterns = [
    path('bank_account/<int:client_id>', BankAccountListApiView.as_view()),
    path('bank_accounts/', BankAccountListApiView.as_view()),
    path('addresses/', AddressListApiView.as_view()),
    path('clients/', ClientsListApiView.as_view()),
    path('account_types/', AccountTypeApiView.as_view()),
    path('currency/', CurrencyApiView.as_view())
]