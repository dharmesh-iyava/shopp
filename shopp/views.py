from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.all()
            for u in user:
                if u.username == username:
                    messages.info(request, 'UserName is Already Exist')
                    return redirect('home')
            x = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                         password=password1)
            x.save()
            messages.info(request, 'Registration successfull')
            return redirect('home')
        else:
            messages.info(request, "Please..Enter Correct Password")
            return redirect('home')

    else:
        return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Logging successfull')
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username Or Password')
            return redirect('home')
    else:
        return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'home.html'


class StoreView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'store.html'
    login_url = '/'


class cart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            return render(self.request, 'cart.html', {'object': order})
        except ObjectDoesNotExist:
            order = {'get_total': 0, 'get_total_count': 0}
            return render(self.request, 'cart.html', {'object': order})
    login_url = '/'


class checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        for order_item in OrderItem.objects.all():
            order_item.ordered = True
            order_item.save()
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            return render(self.request, 'checkout.html', {'object': order})
        except ObjectDoesNotExist:
            messages.error(
                self.request, 'Your Cart Is Empty')
            return redirect('cart')

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            if self.request.method == 'POST':
                address = self.request.POST['address']
                city = self.request.POST['city']
                state = self.request.POST['state']
                pincode = self.request.POST['pincode']
                phone = self.request.POST['phone']
                payment = UserDetail(address=address, city=city,
                                     state=state, pin_code=pincode, mobile_number=phone)
                payment.save()
                order.ordered = True
                order.save()
                return render(self.request, 'success.html')
            return render(self.request, 'checkout.html', {'object': order})
        except ObjectDoesNotExist:
            messages.error(
                self.request, 'Your Cart Is Empty')
            return redirect('cart')
    login_url = '/'


class myorder(LoginRequiredMixin, DetailView):
    def get(self, *args, **kwargs):
        try:
            order = OrderItem.objects.filter(
                user=self.request.user, ordered=True)
            return render(self.request, 'myorder.html', {'object': order})
        except ObjectDoesNotExist:
            return render(self.request, 'home.html')
    login_url = '/'


@login_required(login_url='home')
def success(request):
    return render(request, 'success.html')


@login_required(login_url='home')
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This Item Quantity Was Updated')
            return redirect('cart')
        else:
            messages.info(request, 'This Item Is Added To Cart')
            order.items.add(order_item)
            # messages.info(request, 'This Item Quantity Was Updated')
            return redirect('cart')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This Item Is Added To Cart')
    return redirect('cart')


@login_required(login_url='home')
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.info(request, 'This Item Is Remove From Cart')
            return redirect('cart')
        else:
            messages.info(request, 'This Item IS Not In Your Cart')
            return redirect('home', slug=slug)
    else:
        # add a message saying the user doesnot have an order
        messages.info(request, 'You Do Not Have Any Order')
        return redirect('home', slug=slug)


@login_required(login_url='home')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.save()
            messages.info(request, 'This Item Quantity Was Updated')
            return redirect('cart')

        else:
            messages.info(request, 'This Item IS Not In Your Cart')
            return redirect('home', slug=slug)
    else:
        # add a message saying the user doesnot have an order
        messages.info(request, 'You Do Not Have Any Order')
        return redirect('home', slug=slug)
