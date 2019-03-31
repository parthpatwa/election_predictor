from django.urls import path
from group import views

app_name='group'
urlpatterns = [
    path('groups/<int:p_id>', views.groups_list, name='group_list'),
    path('create_group/<int:p_id>', views.create_group, name='create_group'),
]