from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
import json
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login') 

def c_canteen_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        menu_items = MenuItem.objects.all()
        try:
            student_instance = Student.objects.get(student_id=UUID(user_id))
            context = {'student_instance': student_instance, 'teacher_instance': None, 'user_type': 'student','menu_items': menu_items}
            return render(request, 'canteen/c_canteen.html', context)
        except Student.DoesNotExist:
            try:
                # If Student is not found, attempt to get a Teacher instance
                teacher_instance = Teacher.objects.get(teacher_id=UUID(user_id))
                context = {'student_instance': None, 'teacher_instance': teacher_instance, 'user_type': 'teacher', 'menu_items': menu_items}
                return render(request, 'canteen/c_canteen.html', context)
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
    try:
        user_id = request.session.get('user_id')
        admin_instance = Admin.objects.get(admin_id=UUID(user_id))
    except Admin.DoesNotExist:
        raise Http404("Admin not found")
    order_items = Order.objects.all()
    order_data=[]
    for order in order_items:
        try:
            student_instance = Student.objects.get(student_id=order.customer_id)
            customer_img = student_instance.image.url
        except Student.DoesNotExist:
            try:
                teacher_instance = Teacher.objects.get(teacher_id=order.customer_id)
                customer_img = teacher_instance.image.url
            except Teacher.DoesNotExist:
                raise Http404("User not found")
        order_data.append({
            'order': order,
            'customer_img': customer_img,
        })
    return render(request, 'canteen/orders.html', {'admin_instance': admin_instance, 'order_items': order_data})

@require_POST
# @login_required
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
@csrf_protect
# @login_required
def delete_menuItem(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')

    item = get_object_or_404(MenuItem, pk=item_id)
    item.delete()

    return JsonResponse({'message': 'Item deleted successfully'})

@csrf_protect
# @login_required
def delete_specialItem(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')

    item = get_object_or_404(MenuItem, id=item_id)
    item.special = False
    item.save()
    
    return JsonResponse({'message': 'Item deleted successfully'})

def order_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        customer_id = data.get('customer_id')
        created_at = data.get('created_at')
    return JsonResponse({'message': 'Item not found'})

    #     try:
    #         student = Student.objects.get(student_id=customer_id)
    #         customer_name = student.name
    #         customer_image = student.profile_picture.url
    #         user_type = 'student'
    #     except Student.DoesNotExist:
    #         try:
    #             teacher = Teacher.objects.get(teacher_id=customer_id)
    #             customer_name = teacher.name
    #             customer_image = teacher.profile_picture.url
    #             user_type = 'teacher'
    #         except Teacher.DoesNotExist:
    #             return JsonResponse({'message': 'Customer not found'}, status=404)
    #     try:
    #         item = MenuItem.objects.get(id=item_id)
    #         item_name = item.name
    #         item_price = item.price
    #         item_image = item.image.url
    #     except MenuItem.DoesNotExist:
    #         return JsonResponse({'message': 'Item not found'}, status=404)

    #     response_data = {
    #         'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
    #         'customer_name': customer_name,
    #         'customer_image': customer_image,
    #         'customer_id':customer_id,
    #         'user_type': user_type,
    #         'item_id':item_id,
    #         'item_name': item_name,
    #         'item_price': item_price,
    #         'item_image': item_image,
    #         'quantity':quantity,
    #     }

    #     return JsonResponse(response_data, status=200)

    # return JsonResponse({'message': 'Invalid request method'}, status=400)

def confirm_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        customer_id = data.get('customer_id')
        created_at = data.get('created_at')
        try:
            student = Student.objects.get(student_id=UUID(customer_id))
            name=student.name
        except Student.DoesNotExist:
            try:
                teacher = Teacher.objects.get(teacher_id=UUID(customer_id))
                name=teacher.name
            except Teacher.DoesNotExist:
                return JsonResponse({'message': 'Customer not found'}, status=404)
        menu_item = get_object_or_404(MenuItem, id=item_id)
        order = Order(
            customer_id = UUID(customer_id),
            customer_type =name,
            order_name=menu_item,
            quantity=quantity,
            created_at=created_at,
            status='in-progress',
        )
        order.save()
        return JsonResponse({'message': 'Order confirmed successfully'})    
    return JsonResponse({'message': 'Invalid request method'}, status=400)
