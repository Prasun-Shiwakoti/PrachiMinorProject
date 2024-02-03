from django.shortcuts import render 
from core.models import Admin
from django.http import Http404

def examsection_view(request, user):
    try:
        admin_instance = Admin.objects.get(id=user)
        context = {'admin_instance': admin_instance}
        print('adminid:', admin_instance.id)
        return render(request, 'examsection/exam.html', context)
    except Admin.DoesNotExist:
        raise Http404 ("admin not found")