from django.urls import path, include

app_name = 'party'
urlpatterns = [
    path('group/', include('group.urls'))
]