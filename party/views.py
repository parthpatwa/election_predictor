from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authentication.models import Party, Usertype


# Create your views here.
def party(request):
    party = Party.objects.get(party__user__exact=request.user)
    return render(request, 'party/party.html', {'party': party})


def data_analysis(request):
    usertype = Usertype.objects.get(user_id=request.user.pk)
    if usertype.is_party:
        profile = Party.objects.get(party__user_id=usertype.pk)
        return render(request, 'party/data_analysis.html', {'profile': profile})


def decrease_credits(request, amount=None):
    if amount:
        usertype = Usertype.objects.get(user_id=request.user.pk)
        if usertype.is_party:
            profile = Party.objects.get(party__user_id=usertype.pk)
            if profile.credit_amount >= amount:
                profile.credit_amount = profile.credit_amount - amount
                profile.save()
                return HttpResponseRedirect(reverse('authentication:party:data_analysis'))
            else:
                error = 'You don\'t have enough credits'
                return render(request, 'party/data_analysis.html', {'profile': profile, 'error': error})


def sentiment_analysis_single(request):
    return None


def sentiment_analysis_batch(request):
    return None