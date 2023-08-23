from django.contrib import admin
from django.urls import path, include

from exam.views import index_main

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_panel'),
    path('', index_main, name='main'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('exam.urls')),
    path('users/', include('users.urls'))
]
