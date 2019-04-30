from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import *
from authentication.models import Party, Usertype
import uuid

@login_required(login_url='login')
def predict_review(request):
    result = ''
    review_ph = "Enter your review here"
    if request.method == 'POST':
        review = request.POST['review']
        review_ph = review
        clean = cleantext(review)
        pred = mov.predict([clean])
        if pred[0] == 'p':
            result = 'positive'
        elif pred[0] == 'n':
            result = 'negative'
    context = {'review_ph': review_ph, 'result': result}
    return render(request, 'predictReview/predict.html', context)#change


@login_required(login_url='login')
def batch_predict(request):
    result = ''
    if request.method == 'POST':
    	usertype = Usertype.objects.get(user_id = request.user.pk)
    	if usertype.is_party:
    		profile = Party.objects.get(party__user_id = usertype.pk)
        	temp = profile.credit_amount
        bal = float(temp) - float(200)
        if bal >= 0:
            file1 = request.FILES.get('fileupload')
            review_type = request.POST.get('type')
            if file1 == None:
                result = 'No file uploaded.'
                return render(request, 'predictReview/batch_predict.html', {'result': result})

            ext = file1.name
            if ((not ".txt" in ext) or (file1.content_type != 'text/plain')) and (
                    (not ".csv" in ext) or (file1.content_type != 'application/vnd.ms-excel')):
                result = 'Please upload .txt or .csv file only.'
                return render(request, 'predictReview/batch_predict.html', {'result': result})

            lst = file1.read().splitlines()
            nlist = []
            for i in lst:
                nlist.append(i.decode('utf-8'))

            clean = map(cleantext, nlist)
            pred = mov.predict(clean)
            pos_count = 0
            neg_count = 0
            pos_per = 0
            for i in pred:
                if i == 'p':
                    pos_count += 1  # send to django
                elif i == 'n':
                    neg_count += 1  # send to django
            total_count = pos_count + neg_count  # send to django
            pos_per = pos_count / total_count * 100  # send to django
            result = "Positive review: " + str(pos_count) + "\nNegative review: " + str(
                neg_count) + "\nPercentage of positive review: " + str(pos_per) + "%"
            # temp = AccountBalance.objects.get(user = request.user)
            # bal = float(temp.balance)-float(50)
            profile.credits_amount = bal
            profile.save()
            # return render(request, 'predictReview/batch_predict.html', {'result' : result})
        else:
            result = "Insufficient Credits "

    return render(request, 'predictReview/batch_predict.html', {'result': result})#change
