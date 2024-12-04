from django.urls import path
from . import views

urlpatterns = [
    path('', views.december_calendar, name='december_calendar'),
]

