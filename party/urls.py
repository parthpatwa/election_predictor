from django.urls import path, include
from . import views


app_name = 'party'
urlpatterns = [
    path('', views.party,name='party'),
    path('data_analysis/', views.data_analysis, name='data_analysis'),
    path('decrease_credits/<int:amount>', views.decrease_credits, name='decrease_credits'),
    path('sentimentanalysis/', include('sentimentanalysis.urls')),
]