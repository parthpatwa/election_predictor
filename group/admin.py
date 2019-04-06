from django.contrib import admin

from group.models import Group, Event, GroupMembers
# Register your models here.
admin.site.register([Group, GroupMembers, Event])