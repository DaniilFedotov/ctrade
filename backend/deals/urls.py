from django.urls import path

from . import views

app_name = 'deals'

urlpatterns = [
    path('deals/', views.deals, name='deals'),
    path('traders/', views.traders, name='traders'),
]