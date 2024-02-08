from django.shortcuts import render 
from core.models import Admin
from uuid import UUID
from django.http import Http404

def examsection_view(request):
    user_id = request.session.get('user_id')
    try:
        admin_instance = Admin.objects.get(admin_id=UUID(user_id))
        return render(request, 'examsection/exam.html', {'admin_instance': admin_instance})
    except Admin.DoesNotExist:
        raise Http404("Admin not found")