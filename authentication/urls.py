from django.urls import path, re_path, include
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('login_party/', views.login_party, name='login_party'),
    path('logout/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_party/', views.register_party, name='register_party'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('group/', include('group.urls'))
]
