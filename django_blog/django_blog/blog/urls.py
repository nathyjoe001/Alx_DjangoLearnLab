from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),  # This points to the home view
]
