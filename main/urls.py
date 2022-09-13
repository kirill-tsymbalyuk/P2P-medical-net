from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='home'),
    path('login/', login, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('med-card/', med_card, name='med-card'),
    path('profile/', profile, name='profile'),
    path('get-qrcode/', download_qrcode, name='get-qrcode'),
    path('registration/', registration, name='registration'),
    path('api/', include('rest_framework.urls')),
    path('api/get-history/', get_history),
    path('api/set-data/', set_data)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
