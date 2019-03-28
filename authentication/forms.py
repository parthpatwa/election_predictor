from django import forms
from django.contrib.auth.models import User
from authentication.models import UserProfile


class Registration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password Here ...'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password ...'}))

    class Meta:
        model = User
        fields = ('username','email')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        return confirm_password
