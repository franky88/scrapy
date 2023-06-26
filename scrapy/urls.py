from django.urls import path
from . import views

app_name = "scrapy"
urlpatterns = [
    path('', views.ScrapyView.as_view(), name='home'),
]