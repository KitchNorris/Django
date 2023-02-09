from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('polls/', include('polls.urls')),
    re_path(r'^admin/', admin.site.urls),
    path('', include('api.urls')),
    re_path(r'^users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

