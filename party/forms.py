from django import forms
from party.models import PaymentDetails
from django.forms import ValidationError


def cvv_validate(cvv):
    if len(str(cvv)) != 10:
        raise ValidationError('The CVV must have 3 digits only')
    elif cvv < 0:
        raise ValidationError('The phone number must be positive')


def card_number_validate(cnum):
    if len(str(cnum)) != 16:
        raise ValidationError('The Card number must have 16 digits only')
    elif cnum < 0:
        raise ValidationError('The phone number must be positive')


class PaymentsForm(forms.ModelForm):
    card_number = forms.IntegerField(validators=[card_number_validate])
    card_name = forms.CharField(max_length=1000)
    cvv = forms.CharField(widget=forms.PasswordInput(), validators=[cvv_validate])

    class Meta:
        model = PaymentDetails
        fields = ['credits']
