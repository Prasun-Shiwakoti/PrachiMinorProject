from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order
from django.http import Http404

def c_canteen_view(request, user):
    try:
        student_instance = Student.objects.get(id=user)
        context = {'student_instance': student_instance, 'teacher_instance': None, 'user_type': 'student'}
        return render(request, 'canteen/c_canteen.html', context)
    except Student.DoesNotExist:
        try:
            teacher_instance = Teacher.objects.get(id=user)
            context = {'student_instance': None, 'teacher_instance': teacher_instance, 'user_type': 'teacher'}
            return render(request, 'canteen/c_canteen.html', context)
        except Teacher.DoesNotExist:
            raise Http404("User not found")

def s_canteen_view(request, user):
    try:
        admin_instance = Admin.objects.get(id=user)
        context = {'admin_instance': admin_instance}
        return render(request, 'canteen/s_canteen.html', context)
    except Admin.DoesNotExist:
        raise Http404 ("admin not found")
    
def orders_view(request, user):
    try:
        admin_instance = Admin.objects.get(id=user)
        order_instance = Order.objects.get(admin=admin_instance)
        context = {'admin_instance': admin_instance, 'order_instance': order_instance}
        return render(request, 'canteen/orders.html', context)
    except Admin.DoesNotExist:
        raise Http404("Admin not found")
    except Order.DoesNotExist:
        raise Http404("Order not found")
