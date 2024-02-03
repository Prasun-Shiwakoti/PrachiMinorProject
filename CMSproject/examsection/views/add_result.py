from django.http import JsonResponse
from core.models import Admin
from django.http import Http404
from django.views.decorators.http import require_POST
from examsection.forms.add_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.views import View
from examsection.forms.add_result import upload_result_form
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


def addresult_view(request, semester, batch, faculty, exam_type, user):
    try:
        admin_instance = get_object_or_404(Admin, id=user)
    except Admin.DoesNotExist:
        raise Http404("Admin not found")

    # Pass data to the template
    context = {
        'admin_instance': admin_instance,
        'semester': semester,
        'batch': batch,
        'faculty': faculty,
        'exam_type': exam_type,
    }
    return render(request, 'examsection/add_result.html', context)

class upload_result_file(View):
    template_name = 'add_result.html'

    def get(self, request, *args, **kwargs):
        form = upload_result_form()
        return render(request, self.template_name, {'form': form})

    

