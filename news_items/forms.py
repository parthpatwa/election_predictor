from django import forms

from .models import Query

class FeedForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('query',)
