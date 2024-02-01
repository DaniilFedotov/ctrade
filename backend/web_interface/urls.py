from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('deals/', include('deals.urls', namespace='deals')),
    path('traders/', include('traders.urls', namespace='traders')),
]
