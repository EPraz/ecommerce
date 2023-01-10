from django.shortcuts import redirect, render
from django.http import JsonResponse

import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import *

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def store(request):

    data = cartData(request)    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

  
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, "store/Store.html", context)

def cart(request):
    
    data = cartData(request)    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,

    }
    return render(request, "store/Cart.html", context)

def checkout(request):
    
    data = cartData(request)    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, "store/Checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print("Action:", action)
    # print("productId:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    # print("Data:", request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
        customer, order = guestOrder(request, data)
        

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            # zipcode = data['shipping']['zipcode']
        )

    return JsonResponse('Payment complete!', safe=False)



# Create Products View
class AddProductView(LoginRequiredMixin, CreateView):
    template_name = "store/add_product.html"
    model = Product
    form_class = ProductForm

class UpdateProductView(LoginRequiredMixin, UpdateView):
    template_name = 'store/update_product.html'
    model = Product
    form_class = ProductForm

class DeleteProductView(LoginRequiredMixin, DeleteView):
    template_name = 'store/delete_product.html'
    success_url = '/'
    model = Product

class ViewProductPage(TemplateView):
    template_name = 'store/view_product.html'
    model = Product


# def ViewProductPage(request):

#     data = cartData(request)    
#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']

#     context = {
#         'items': items,
#         'order': order,
#         'cartItems': cartItems,

#     }
#     return render(request, "store/view_product.html", context)


    

# Login / Logout
def log_out(request):
    logout(request)
    return redirect('/')