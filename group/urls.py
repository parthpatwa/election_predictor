from django.urls import path
from group import views

app_name='group'
urlpatterns = [
    path('groups_list/<int:p_id>', views.groups_list, name='group_list'),
    path('create_group/<int:p_id>', views.create_group, name='create_group'),
    path('event_list/<int:g_id>', views.event_list, name='event_list'),
    path('create_event/<int:g_id>', views.create_event, name='create_event'),
]