from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .data_analysis import get_stats,get_fav
#from one_page.models import *
import pandas as pd
#from credits.models import AccountBalance,Statement
from django.http import HttpResponse
import uuid

# Create your views here.
@login_required(login_url='login')
def main_view(request):
    context = {'options': options.keys()}
    return render(request, 'dataAnalysis/main_page.html', context=context)



def stats(request):
    if request.method == 'POST':
        temp = AccountBalance.objects.get(user=request.user)
        if float(temp.balance) > 200:
            complete = pd.read_csv(dct)

            total_stats,pos_stats,neg_stats = get_stats(complete,name,option)#send to django
            posper = pos_stats['count']/total_stats['count']*100
            negper = neg_stats['count']/total_stats['count']*100
            context = {'new_count':unlabeled_count,'posper':posper,'negper':negper,
            'total_stats':total_stats,'pos_stats':pos_stats,'neg_stats':neg_stats,
            'type':option,'name':name}
            AccountBalance.objects.filter(user=request.user).update(balance=temp.balance-200)
            Statement.objects.create(user=request.user,transaction_id="PSA"+uuid.uuid4().hex[:9].upper(),amount=200)
            return render(request, 'dataAnalysis/graphs.html', context)
        else:
            return HttpResponse('<html><head><script>alert("You dont have sufficient funds");window.location="/data_analysis";</script></head></html>')
    else:
        #return HttpResponse(status = 400)
        return redirect('data_analysis')
def get_title(gender,rtype):
    option1 = options[rtype]
    lst = option1.objects.all()#list of movies
    names = []
    genders = []
    polarities = []
    for i in lst:
        rev_objs = i.labeled.all()
        fields = dict(i.get_fields())
        for j in rev_objs:
            names.append(i.title)
            if j.polarity:
                polarities.append('p')
            else:
                polarities.append('n')
            genders.append(j.user.userprofile.gender)
    dct = {rtype:names,'polarity':polarities,'gender':genders}
    complete = pd.DataFrame(dct)
    title = get_fav(complete,gender,rtype)
    return title

