from django import forms
from group.models import Group, Event


class GroupRegistration(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class EventRegistration(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date']
