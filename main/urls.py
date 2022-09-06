from django.urls import path, include
from .views import *

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('get-history', get_history)
]
