from django.contrib import admin

from group.models import Group, Event, Group_members
# Register your models here.
admin.site.register([Group, Group_members, Event])