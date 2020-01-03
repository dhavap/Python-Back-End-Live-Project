from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.space_exploration, name='explore'),
    path('<str:decade>/result/', views.result, name='result'),
]




