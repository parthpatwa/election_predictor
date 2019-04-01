from django import forms
from group.models import Group


class groupRegistration(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
