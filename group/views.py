from django.shortcuts import render, redirect
from group.forms import groupRegistration, eventRegistration

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


def create_group(request, p_id=None):
    if p_id:
        form = groupRegistration()
        if request.method == 'POST':
            form = groupRegistration(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']

                with connection.cursor() as cursor:
                    cursor.execute('select authentication_party.id from authentication_party where party_id = %s',
                                   [p_id])
                    admin_id = cursor.fetchone()[0]

                with connection.cursor() as cursor:
                    cursor.execute('insert into group_group(name, description, admin_id_id) values (%s,%s,%s)',
                                   [name, description, admin_id])

                with connection.cursor() as cursor:
                    cursor.execute(
                        'select * from group_group where admin_id_id = (select id from authentication_party where party_id = %s)',
                        [p_id])
                    groups = cursor.fetchall()
                return render(request, 'group/group_list.html', {'groups': groups})
        else:
            return render(request, 'group/create_group.html', {'form': form})


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
        form = eventRegistration()
        if request.method == 'POST':
            form = eventRegistration(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                day = form.cleaned_data['day']
                location = form.cleaned_data['location']
                # group_id = Group.objects.get(pk=g_id)
                # with connection.cursor() as cursor:
                #     cursor.execute('select group_group.id from group_group where admin_id_id = %s', [g_id])
                #     admin_id = cursor.fetchone()[0]
                # Event.objects.create(name=name, description=description,
                #                      date=date, day=day, location=location,
                #                      group_id=group_id)
                with connection.cursor() as cursor:
                    cursor.execute(
                        'insert into group_event(name, description, location, date, day, group_id_id) values (%s, %s, %s, %s, %s, 0%s)',
                        [name, description, location, date, day, g_id])
                with connection.cursor() as cursor:
                    cursor.execute('select * from group_event where group_id_id = %s', [g_id])
                    event = cursor.fetchall()
                return render(request, 'group/event_list.html', {'event': event, 'g_id': g_id})
        else:
            return render(request, 'group/create_event.html', {'form': form, })
