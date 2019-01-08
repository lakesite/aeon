from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include('api.urls')),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  path('', lambda request: redirect('api/')),
]
