from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('registration/', registration, name='registration'),
    path('api/', include('rest_framework.urls')),
    path('api/get-history/', get_history),
    path('api/set-data/', set_data)
]
