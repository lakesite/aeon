from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path('', lambda request: redirect('v1/')),
    path('v1/', include('aeon.urls')),
]
