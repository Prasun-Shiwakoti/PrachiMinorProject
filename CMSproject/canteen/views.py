from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
import json
from uuid import UUID
from django.shortcuts import get_object_or_404

def c_canteen_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        menu_items = MenuItem.objects.all()
        try:
            student_instance = Student.objects.get(student_id=UUID(user_id))
            context = {'student_instance': student_instance, 'teacher_instance': None, 'user_type': 'student'}
            return render(request, 'canteen/c_canteen.html', {'context': context, 'menu_items': menu_items})
        except Student.DoesNotExist:
            try:
                # If Student is not found, attempt to get a Teacher instance
                teacher_instance = Teacher.objects.get(teacher_id=UUID(user_id))
                context = {'student_instance': None, 'teacher_instance': teacher_instance, 'user_type': 'teacher'}
                return render(request, 'canteen/c_canteen.html', {'context': context, 'menu_items': menu_items})
            except Teacher.DoesNotExist:
                raise Http404("User not found")
    else:
        raise Http404("User ID not found in session")

def s_canteen_view(request):
    try:
        user_id = request.session.get('user_id')
        admin_instance = Admin.objects.get(admin_id=UUID(user_id))
    except Admin.DoesNotExist:
        raise Http404("Admin not found")
    menu_items = MenuItem.objects.all()
    # Pass menu items along with admin_instance to the template
    return render(request, 'canteen/s_canteen.html', {'admin_instance': admin_instance, 'menu_items': menu_items})
def orders_view(request):
    user_id = request.session.get('user_id')
    try:
        admin_instance = Admin.objects.get(admin_id=UUID(user_id))
        # order_instance = Order.objects.get(admin=admin_instance)
        context = {'admin_instance': admin_instance}
        return render(request, 'canteen/orders.html', context)
    except Admin.DoesNotExist:
        raise Http404("Admin not found")
    except Order.DoesNotExist:
        raise Http404("Order not found")

@require_POST
@login_required
@csrf_protect
def add_menuItem(request):
    try:
        item_name = request.POST.get('itemsName')
        item_price = request.POST.get('itemsPrice')
        item_description = request.POST.get('itemsDescription')
        item_image = request.FILES.get('itemsImageInput')

        new_item = MenuItem(name=item_name, price=item_price, description=item_description, image=item_image)
        new_item.save()

        response_data = {
            'message': 'Item added successfully',
            'item': {
                'name': new_item.name,
                'price': new_item.price,
                'description': new_item.description,
                'image_url': new_item.image.url,
            }
        }

        return JsonResponse(response_data)
    except Exception as e:
        print(f"Error in add_menuItem view: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@csrf_protect
def add_specialItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_name = data.get('itemName')
        special_status = data.get('special', False)

        # Update the MenuItem's special status
        menu_item = get_object_or_404(MenuItem, name=item_name)
        menu_item.special = special_status
        menu_item.save()

        return JsonResponse({'message': 'Special status updated successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
