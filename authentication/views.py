from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from authentication.forms import Registration, PartyRegistration, CreateProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime  import datetime

from authentication.models import Party, Usertype
from authentication.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.db import connection


def registration_all(request):
    return render(request, 'authentication/registration_all.html')


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # ut = Usertype.objects.filter(user=user, is_user=True)
            with connection.cursor() as cursor:
                cursor.execute('select * from authentication_usertype where user_id = %s and is_user = %s', [user.pk, True])
                ut = cursor.fetchall()
            if len(ut) == 1:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                if 'next' in request.GET:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('news_items:articles_list')
            else:
                return HttpResponse('User does not exist')

    return render(request, 'authentication/login.html', {'form': form})


def login_party(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # ut = Usertype.objects.filter(user=user, is_party=True)
            with connection.cursor() as cursor:
                cursor.execute('select * from authentication_usertype where user_id = %s and is_party = %s', [user.pk, True])
                ut = cursor.fetchall()
            if len(ut) == 1:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return render(request, 'party/party.html')
            else:
                return HttpResponse('Party does not exist')

    return render(request, 'authentication/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'authentication/logout.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('authentication:login_user')
    else:
        return HttpResponse('Activation link is invalid!')


def register_user(request):
    form = Registration()
    form_profile = CreateProfile()
    if request.method == 'POST':
        form = Registration(request.POST)
        form_profile = CreateProfile(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # ut = Usertype.objects.create(user=user, is_user=True)
            # ut.save()
            with connection.cursor() as cursor:
                cursor.execute('insert into authentication_usertype(user_id, is_user, is_party) values (%s,%s,%s)',
                               [user.pk, True, False])

            # profile = form_profile.save(commit=False)
            # profile.profile = ut
            # profile.save()
            first_name = form_profile.cleaned_data['first_name']
            last_name = form_profile.cleaned_data['last_name']
            phone_num = form_profile.cleaned_data['phone_num']
            location = form_profile.cleaned_data['location']
            gender = form_profile.cleaned_data['gender']
            with connection.cursor() as cursor:
                cursor.execute('insert into authentication_profile(first_name, last_name, phone_num, location, gender, profile_id) values (%s,%s,%s, %s,%s,%s)', [first_name, last_name, phone_num, location, gender, user.pk])

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authentication/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    return render(request, 'authentication/register.html', {'form': form, 'form_profile': form_profile})


def register_party(request):
    form_basic = Registration()
    form_party = PartyRegistration()
    if request.method == 'POST':
        form_basic = Registration(request.POST)
        form_party = PartyRegistration(request.POST)
        if form_basic.is_valid() and form_party.is_valid():
            user = form_basic.save(commit=False)
            description = form_party.cleaned_data['description']
            name = form_party.cleaned_data['name']
            user.set_password(form_basic.cleaned_data['password'])
            user.save()

            # ut = Usertype.objects.create(user=user, is_party=True)
            # ut.save()
            with connection.cursor() as cursor:
                cursor.execute('insert into authentication_usertype(user_id, is_user, is_party) values (%s,%s,%s)', [user.pk, False, True])
            # party = Party.objects.create(party=ut, description=description, name=name)
            # party.save()
            with connection.cursor() as cursor:
                cursor.execute('insert into authentication_party(name, description, created_at, credit_amount,party_id) values (%s,%s,%s,%s,%s)', [name, description, datetime.now(), 0, user.pk])


            return HttpResponse('Party successfully created.')

    return render(request, 'authentication/register.html',
                  {'form': form_basic, 'form_party': form_party})
