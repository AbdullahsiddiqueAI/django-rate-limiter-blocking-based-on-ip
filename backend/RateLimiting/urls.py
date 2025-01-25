from django.urls import path
from .views import *
urlpatterns = [
    path("request-status/", request_status_view, name="request_status"),
]
