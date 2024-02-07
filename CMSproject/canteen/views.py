from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem
from django.views.decorators.http import require_POST
from django.http import Http404, JsonResponse
from uuid import UUID
def c_canteen_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            student_instance = Student.objects.get(student_id=UUID(user_id))
            context = {'student_instance': student_instance, 'teacher_instance': None, 'user_type': 'student'}
            return render(request, 'canteen/c_canteen.html', context)
        except Student.DoesNotExist:
            try:
                # If Student is not found, attempt to get a Teacher instance
                teacher_instance = Teacher.objects.get(teacher_id=UUID(user_id))
                context = {'student_instance': None, 'teacher_instance': teacher_instance, 'user_type': 'teacher'}
                return render(request, 'canteen/c_canteen.html', context)
            except Teacher.DoesNotExist:
                raise Http404("User not found")
    else:
        raise Http404("User ID not found in session")

def s_canteen_view(request):
    user_id = request.session.get('user_id')
    try:
        admin_instance = Admin.objects.get(admin_id=UUID(user_id))
        return render(request, 'canteen/s_canteen.html', {'admin_instance': admin_instance})
    except Admin.DoesNotExist:
        raise Http404("Admin not found")

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
def add_item(request):
    item_name = request.POST.get('itemsName')
    item_price = request.POST.get('itemsPrice')
    item_image = request.FILES.get('itemsImageInput')
            # Create a new MenuItem object and save it to the database
    new_item = MenuItem(name=item_name, price=item_price, image=item_image)
    new_item.save()
    response_data = {
        'message': 'Item added successfully',
        'item': {
            'name': new_item.name,
            'price': new_item.price,
            'image_url': new_item.image.url,
        }
    }
    # Send a JSON response back to the JavaScript code
    return JsonResponse(response_data)
  

def get_menu_items(request):
    menu_items = MenuItem.objects.all()
    data = [{'name': item.name, 'price': item.price, 'image_url': item.image.url} for item in menu_items]
    return JsonResponse({'menu_items': data})

