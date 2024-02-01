from django.urls import path

from . import views

app_name = 'deals'

urlpatterns = [
    path('deals/', views.deals, name='deal'),
    path('traders/', views.traders, name='trader'),
]
