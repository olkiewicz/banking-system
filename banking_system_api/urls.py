from django.urls import re_path, path
from .views import (
    AccountApiView, AddressApiView, ClientsListApiView, AccountTypeApiView, CurrencyApiView,
)

urlpatterns = [
    re_path(r'^accounts/(?P<account_id>[0-9]*)', AccountApiView.as_view()),
    re_path(r'^addresses/(?P<address_id>[0-9]*)', AddressApiView.as_view()),
    re_path(r'^clients/(?P<client_id>[0-9]*)', ClientsListApiView.as_view()),
    re_path(r'^account_types/(?P<account_type_id>[0-9]*)', AccountTypeApiView.as_view()),
    re_path(r'^currencies/(?P<currency_id>[0-9]*)', CurrencyApiView.as_view())
]
