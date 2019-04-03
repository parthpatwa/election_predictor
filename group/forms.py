from django import forms
from group.models import Group, Event


class groupRegistration(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class eventRegistration(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'day']
