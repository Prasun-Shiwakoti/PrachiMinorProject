from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem, Notification
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
import json
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login:login')
 
@login_required
def c_canteen_view(request):
    user = request.user  # Django's authenticated user
    menu_items = MenuItem.objects.all()

    if user.usertype == 'student':
        student_instance = user.student
        context = {'student_instance': student_instance, 'teacher_instance': None, 'user_type': 'student', 'menu_items': menu_items}
        return render(request, 'canteen/c_canteen.html', context)
    elif user.usertype == 'teacher':
        teacher_instance = user.teacher
        context = {'student_instance': None, 'teacher_instance': teacher_instance, 'user_type': 'teacher', 'menu_items': menu_items}
        return render(request, 'canteen/c_canteen.html', context)
    else:
        raise Http404("User not found")
    
@login_required
def s_canteen_view(request):
    user = request.user  # Django's authenticated user
    menu_items = MenuItem.objects.all()

    if user.usertype == 'admin':
        admin_instance = user.admin
        context = {'admin_instance': admin_instance, 'menu_items': menu_items}
        return render(request, 'canteen/s_canteen.html', context)
    else:
        raise Http404("Admin not found")
    
@login_required
def orders_view(request):
    user = request.user  # Django's authenticated user
    order_items = Order.objects.all()
    order_data = []

    for order in order_items:
        customer = order.customer
        try:
            if customer.usertype == 'student':
                customer_instance = customer.student
                customer_img = customer_instance.profile_picture.url
            elif customer.usertype == 'teacher':
                customer_instance = customer.teacher
                customer_img = customer_instance.profile_picture.url
            else:
                raise Http404("User not found")
        except (Student.DoesNotExist, Teacher.DoesNotExist):
            raise Http404("User not found")

        order_data.append({
            'order': order,
            'customer_img': customer_img,
        })

    context = {'admin_instance': user.admin, 'order_items': order_data}
    return render(request, 'canteen/orders.html', context)


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
def delete_menuItem(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')

    item = get_object_or_404(MenuItem, pk=item_id)
    item.delete()

    return JsonResponse({'message': 'Item deleted successfully'})

@csrf_protect
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
@login_required
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
            customerObj = student
        except Student.DoesNotExist:
            try:
                teacher = Teacher.objects.get(teacher_id=UUID(customer_id))
                name=teacher.name
                customerObj = teacher
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
        
        push_notification = Notification.objects.create(title="Order Confirmed", content="Your order of {quantity} {menu_item.name} has been confirmed.")
        customerObj.notifications.add(push_notification)

        return JsonResponse({'message': 'Order confirmed successfully'})    
    return JsonResponse({'message': 'Invalid request method'}, status=400)
