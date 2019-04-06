from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from group.forms import GroupRegistration, EventRegistration
from .models import GroupMembers, Group, Event
from authentication.models import Profile, Usertype, Party
from django.db import connection


def groups_list(request, p_id=None):
    if p_id:
        with connection.cursor() as cursor:
            cursor.execute(
                'select * from group_group where admin_id_id = (select id from authentication_party where party_id = %s)',
                [p_id])
            groups = cursor.fetchall()

            return render(request, 'group/group_list.html', {'groups': groups})
    else:
        return redirect('authentication:login_user')


@login_required
def create_group(request, p_id=None):
    if p_id:
        form = GroupRegistration()
        if request.method == 'POST':
            form = GroupRegistration(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']

                with connection.cursor() as cursor:
                    cursor.execute('select authentication_party.id from authentication_party where party_id = %s',
                                   [p_id])
                    admin_id = cursor.fetchone()[0]
                try:
                    with connection.cursor() as cursor:
                        cursor.execute('insert into group_group(name, description, admin_id_id) values (%s,%s,%s)',
                                       [name, description, admin_id])
                except:
                    return render(request, 'group/create_group.html',
                                  {'form': form, 'error': 'This group already exists'})

                with connection.cursor() as cursor:
                    cursor.execute(
                        'select * from group_group where admin_id_id = (select id from authentication_party where party_id = %s)',
                        [p_id])
                    groups = cursor.fetchall()
                return render(request, 'group/group_list.html', {'groups': groups})
        else:
            return render(request, 'group/create_group.html', {'form': form})


@login_required
def update_group(request, g_id=None):
    if g_id:
        group = Group.objects.get(pk=g_id)
        if request.method == 'POST':
            group_details = GroupRegistration(request.POST, instance=group)
            if group_details.is_valid():
                try:
                    group.name = group_details.cleaned_data['name']
                    group.description = group_details.cleaned_data['description']
                    group.save()
                    party = Party.objects.get(pk=group.admin_id_id)
                    return HttpResponseRedirect(reverse('authentication:group:group_list', args=(party.party_id,)))
                except:
                    return render(request, 'group/edit_group.html',
                                  {'form': group_details, 'error': 'This group already exists'})
        else:
            group_details = GroupRegistration(instance=group)
            return render(request, 'group/edit_group.html', {'form': group_details})


def event_list(request, g_id=None):
    if g_id:
        # event = Event.objects.filter(group_id_id=g_id)
        with connection.cursor() as cursor:
            cursor.execute('select * from group_event where group_id_id = %s', [g_id])
            event = cursor.fetchall()
        return render(request, 'group/event_list.html', {'event': event, 'g_id': g_id})
    else:
        return redirect('authentication:group:group_list')


def create_event(request, g_id=None):
    if g_id:
        form = EventRegistration()
        if request.method == 'POST':
            form = EventRegistration(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                location = form.cleaned_data['location']
                # group_id = Group.objects.get(pk=g_id)
                # with connection.cursor() as cursor:
                #     cursor.execute('select group_group.id from group_group where admin_id_id = %s', [g_id])
                #     admin_id = cursor.fetchone()[0]
                # Event.objects.create(name=name, description=description,
                #                      date=date, day=day, location=location,
                #                      group_id=group_id)
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'insert into group_event(name, description, location, date, group_id_id) values (%s, %s, %s, %s, %s)',
                            [name, description, location, date, g_id])
                except:
                    return render(request, 'group/create_event.html',
                                  {'form': form, 'error': 'This event already exists'})

                with connection.cursor() as cursor:
                    cursor.execute('select * from group_event where group_id_id = %s', [g_id])
                    event = cursor.fetchall()
                return render(request, 'group/event_list.html', {'event': event, 'g_id': g_id})

        else:
            return render(request, 'group/create_event.html', {'form': form, })


def update_event(request, event_id):
    if event_id:
        event = Event.objects.get(pk=event_id)
        if request.method == 'POST':
            event_details = EventRegistration(request.POST, instance=event)
            if event_details.is_valid():
                try:
                    event.name = event_details.cleaned_data['name']
                    event.description = event_details.cleaned_data['description']
                    event.location = event_details.cleaned_data['location']
                    event.date = event_details.cleaned_data['date']
                    event.save()
                    return event_list(request, event.group_id_id)
                except:
                    return render(request, 'group/edit_event.html',
                                  {'form': event_details, 'error': 'This event already exists'})

        else:
            event_details = EventRegistration(instance=event)
            return render(request, 'group/edit_event.html', {'form': event_details})


def members_list(request, g_id=None):
    if g_id:
        group_members = GroupMembers.objects.filter(group_id_id=g_id, status=True)
        user_id = []
        for i in group_members:
            user_id.append(i.user_id_id)
        members = Profile.objects.filter(pk__in=user_id)
        user = Usertype.objects.get(user_id=request.user.pk)
        return render(request, 'group/member_list.html', {'members': members, 'g_id': g_id, 'usertype': user})


def add_group_members(request, g_id=None):
    if g_id:
        group_members = GroupMembers.objects.filter(group_id_id=g_id)
        user_id = []
        for i in group_members:
            user_id.append(i.user_id_id)
        print(user_id)
        party = Group.objects.get(pk=g_id).admin_id
        members = Profile.objects.exclude(pk__in=user_id).filter(party_id=party)
        return render(request, 'group/add_group_members.html', {'members': members, 'g_id': g_id})


def request_member(request, g_id=None, u_id=None):
    if g_id and u_id:
        GroupMembers.objects.create(user_id_id=u_id, group_id_id=g_id)
    return HttpResponseRedirect(reverse('authentication:group:add_group_members', args=(g_id,)))


def requested_members(request, g_id=None):
    if g_id:
        group_members = GroupMembers.objects.filter(group_id_id=g_id, status=False)
        user_id = []
        for i in group_members:
            user_id.append(i.user_id_id)
        members = Profile.objects.filter(pk__in=user_id)
        return render(request, 'group/requested_member_list.html', {'members': members, 'g_id': g_id})


def delete_request(request, g_id=None, u_id=None):
    if g_id and u_id:
        instance = GroupMembers.objects.get(user_id_id=u_id, group_id_id=g_id)
        instance.delete()
    return HttpResponseRedirect(reverse('authentication:group:requested_members', args=(g_id,)))


def user_groups(request, u_id=None):
    if u_id:
        u_id = Profile.objects.get(profile__user_id=u_id)
        group_members = GroupMembers.objects.filter(user_id=u_id, status=True)
        group_id = []
        for i in group_members:
            group_id.append(i.group_id_id)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM group_group WHERE group_group.id IN %s', [group_id])
                groups = cursor.fetchall()
        except:
            groups = ()
        return render(request, 'group/user_group_list.html', {'groups': groups, 'u_id': u_id})


def user_requested(request, u_id=None):
    if u_id:
        u_id = Profile.objects.get(profile__user_id=u_id)
        group_members = GroupMembers.objects.filter(user_id=u_id, status=False)
        group_id = []
        for i in group_members:
            group_id.append(i.group_id_id)
        groups = Group.objects.filter(pk__in=group_id)
        return render(request, 'group/user_requested.html', {'groups': groups, 'u_id': u_id})


def user_accept(request, g_id=None, u_id=None):
    if g_id and u_id:
        instance = GroupMembers.objects.get(user_id_id=u_id, group_id_id=g_id)
        instance.status = True
        instance.save()
    return HttpResponseRedirect(reverse('authentication:group:user_requested', args=(request.user.pk,)))


def user_decline(request, g_id=None, u_id=None):
    if g_id and u_id:
        instance = GroupMembers.objects.get(user_id_id=u_id, group_id_id=g_id)
        instance.delete()
    return HttpResponseRedirect(reverse('authentication:group:user_requested', args=(request.user.pk,)))
