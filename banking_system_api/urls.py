from django.urls import path, include
from .views import (
    AccountListApiView, AddressListApiView, ClientsListApiView, AccountTypeApiView, CurrencyApiView,
)

urlpatterns = [
    path('accounts/<int:client_id>', AccountListApiView.as_view()),
    path('accounts/', AccountListApiView.as_view()),
    path('addresses/', AddressListApiView.as_view()),
    path('clients/', ClientsListApiView.as_view()),
    path('account_types/', AccountTypeApiView.as_view()),
    path('currencies/', CurrencyApiView.as_view())
]