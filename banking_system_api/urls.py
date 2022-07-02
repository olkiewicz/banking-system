from django.conf.urls import url
from django.urls import path, include
from .views import (
    BankAccountListApiView,
)

urlpatterns = [
    path('api', BankAccountListApiView.as_view()),
]