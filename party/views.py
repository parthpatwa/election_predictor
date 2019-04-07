from django.shortcuts import render
from authentication.models import Party
# Create your views here.
def party(request):
        party = Party.objects.get(party__user__exact=request.user)
        return render(request, 'party/party.html', {'party': party})
