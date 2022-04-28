
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import LikeFilter


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'account/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    likes = Like.objects.all()
    members = Member.objects.all()

    total_members = members.count()

    total_likes = likes.count()
    delivered = likes.filter(status='Delivered').count()
    pending = likes.filter(status='Pending').count()

    context = {'orders': likes, 'customers': members,
               'total_orders': total_likes, 'delivered': delivered,
               'pending': pending}

    return render(request, 'account/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'account/products.html', {'products': products})


@login_required(login_url='login')
def member(request, pk_test):
    member = Member.objects.get(id=pk_test)

    likes = member.like_set.all()
    like_count = likes.count()

    myFilter = LikeFilter(request.GET, queryset=likes)
    likes = myFilter.qs

    context = {'member': member, 'likes': likes, 'like_count': like_count,
               'myFilter': myFilter}
    return render(request, 'account/member.html', context)


# @login_required(login_url='login')
# def createOrder(request, pk):
#     OrderFormSet = inlineformset_factory(
#         Customer, Order, fields=('product', 'status'), extra=10)
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
#     #form = OrderForm(initial={'customer':customer})
#     if request.method == 'POST':
#         #print('Printing POST:', request.POST)
#         form = OrderForm(request.POST)
#         formset = OrderFormSet(request.POST, instance=customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect('/')

#     context = {'form': formset}
#     return render(request, 'accounts/order_form.html', context)


# @login_required(login_url='login')
# def updateOrder(request, pk):

#     order = Order.objects.get(id=pk)
#     form = OrderForm(instance=order)

#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('/')

#     context = {'form': form}
#     return render(request, 'accounts/order_form.html', context)


# @login_required(login_url='login')
# def deleteOrder(request, pk):
#     order = Order.objects.get(id=pk)
#     if request.method == "POST":
#         order.delete()
#         return redirect('/')

#     context = {'item': order}
#     return render(request, 'accounts/delete.html', context)
