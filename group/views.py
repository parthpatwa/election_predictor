from django.shortcuts import render, redirect
from group.models import Group
from group.forms import groupRegistration
from authentication.models import Party


# Create your views here.
def groups_list(request, p_id=None):
    if p_id:
        groups = Group.objects.filter(admin_id__party__user_id=p_id)
        return render(request, 'group/group_list.html', {'groups': groups})
    else:
        return redirect('authentication:login_party')


def create_group(request, p_id=None):
    if p_id:
        form = groupRegistration()
        if request.method == 'POST':
            form = groupRegistration(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                admin_id = Party.objects.get(party__user_id=p_id)
                Group.objects.create(name=name, description=description, admin_id=admin_id)
                groups = Group.objects.filter(admin_id__party__user_id=p_id)
                return render(request, 'group/group_list.html', {'groups': groups})
        else:
            return render(request, 'group/create_group.html', {'form': form})



    return None