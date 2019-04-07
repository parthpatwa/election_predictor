from django.urls import path, include
from . import views
app_name = 'party'
urlpatterns = [
    path('', views.party,name='party')

]