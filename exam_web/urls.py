from django.contrib import admin
from django.urls import path, include

from exam.views import index_main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', index_main),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('exam.urls'))
]
