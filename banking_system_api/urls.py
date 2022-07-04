from django.conf.urls import url
from django.urls import path, include
from .views import (
    BankAccountListApiView, AddressListApiView, ClientsListApiView,
)

urlpatterns = [
    path('bank_account/<int:client_id>', BankAccountListApiView.as_view()),
    path('bank_accounts/', BankAccountListApiView.as_view()),
    path('addresses/', AddressListApiView.as_view()),
    path('clients/', ClientsListApiView.as_view())
]