from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .data_analysis import get_stats
import pandas as pd
from authentication.models import Usertype, Party
from django.http import HttpResponse
import uuid

# Create your views here.
@login_required(login_url='login')
def main_view(request):
    context = {'options': options.keys()}
    return render(request, 'dataAnalysis/main_page.html', context=context)



def stats(request):
    if request.method == 'POST':
    	usertype = Usertype.objects.get(user_id = request.user.pk)
    	if usertype.is_party:
    		profile = Party.objects.get(party__user_id = usertype.pk)
        	temp = profile.credit_amount
        	bal = float(temp) - float(200)
        if float(bal) >= 0:
        	name = profile.name
            complete = pd.read_csv('tweets/cleaned_political_tweets.csv')
            pos_stats,neg_stats, opp_pos_count, opp_neg_count , opp_name = get_stats(complete,name)#send to django
            pos_avg_len = pos_stats['avg_text_len']
            neg_avg_len = neg_stats['avg_text_len']
            party_pos_count = pos_stats['count']
            party_neg_count = neg_stats['count']
            g1_y = [party_pos_count,party_neg_count]
            g1_x = ['p','n']
            g2_y = [party_pos_count,opp_pos_count]
            g2_x = [name , opp_name]
            g3_y = [party_neg_count,opp_neg_count]
            g3_x = [name , opp_name]
            g4_y = [party_pos_count+party_neg_count, opp_pos_count+opp_neg_count]
            g4_x = [name , opp_name]
            g1_dct = {'x': g1_x , 'y' : g1_y}
            g2_dct = {'x': g2_x , 'y' : g2_y}
            g3_dct = {'x': g3_x , 'y' : g3_y}
            g4_dct = {'x': g4_x , 'y' : g4_y}
            pos_words = pos_stats['freq_words']
            neg_words = neg_stats['freq_words']
            context = {'g1':g1_dct,'g2':g2_dct,'g3':g3_dct,'g4':g4_dct,'pos_avg_lev':pos_avg_lev , 
            'profile':profile, 'neg_avg_len' : neg_avg_len, 'pos_words': pos_words, 'neg_words':neg_words
            'pos_hash':pos_hash , 'neg_hash',neg_hash}
            profile.credits_amount = bal
            profile.save()
            return render(request, 'dataAnalysis/graphs.html', context)
        else:
            return HttpResponse('<html><head><script>alert("You dont have sufficient funds");window.location="/data_analysis";</script></head></html>')
    else:
        #return HttpResponse(status = 400)
        return redirect('data_analysis')


