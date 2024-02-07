from django.http import JsonResponse
from core.models import Admin
from django.http import Http404
from django.views.decorators.http import require_POST
from examsection.forms.add_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.views import View
from examsection.forms.view_result import UploadResultForm
from django.shortcuts import render, get_object_or_404

@csrf_protect
def handle_filter_submission(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        print(request.POST)

        if form.is_valid():
            filter_metadata = form.get_filter_metadata()
            print("Filter Metadata After Validation:", filter_metadata)
            return JsonResponse({'success': True, 'data': filter_metadata})
        else:
            print("Validation Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})
