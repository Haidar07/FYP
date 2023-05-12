from datetime import date, timedelta
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, User, Cart, OrderedProduct, Reviews
from . import forms
from django.contrib import messages

# Home Page functions


def home_view(request):
    all_products = Product.objects.all()
    if request.method == 'POST':
        form = forms.ProductForm()
        if form.is_valid:
            if request.POST.get('searchby') == 'product_name':
                all_products = Product.objects.filter(
                    product_name__icontains=request.POST.get('search-result'))
            elif request.POST.get('searchby') == 'product_category':
                all_products = Product.objects.filter(
                    product_category__icontains=request.POST.get('search-result'))
    if request.user.is_authenticated:
        return render(request, 'user/user_afterlogin.html', {'all_products': all_products})
    return render(request, 'home/index.html', {'all_products': all_products})


def sortbyname(request):
    all_products = Product.objects.all().order_by('product_name')
    if request.user.is_authenticated:
        return render(request, 'user/user_afterlogin.html', {'all_products': all_products})
    return render(request, 'home/index.html', {'all_products': all_products})


def sortbyprice(request):
    all_products = Product.objects.all().order_by('price')
    if request.user.is_authenticated:
        return render(request, 'user/user_afterlogin.html', {'all_products': all_products})
    return render(request, 'home/index.html', {'all_products': all_products})


def new_arrivals(request):
    all_products = Product.objects.raw(
        "select * from supermarket_app_product where CURRENT_DATE - date_added<3;")

    if request.user.is_authenticated:
        return render(request, 'user/new_arrivals.html', {'all_products': all_products})
    return render(request, 'home/new_arrivals.html', {'all_products': all_products})


# Registration
def usersignup_view(request):
    form1 = forms.UserForm()
    mydict = {'form1': form1}
    if request.method == 'POST':
        form1 = forms.UserForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            # my_admin_group = Group.objects.get_or_create(name='ADMIN')
            # my_admin_group[0].user_set.add(user)
            my_user_group = Group.objects.get_or_create(name='User')
            my_user_group[0].user_set.add(user)
            usr = User.objects.create(user=user)
            usr.save()
        return HttpResponseRedirect('userlogin')
    return render(request, 'regist/usersignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# After Login function
def afterlogin_view(request):
    all_products = Product.objects.all()
    if is_admin(request.user):
        for product in Product.objects.all():
            print(product.date_added)
        return render(request, 'admin/admin_afterlogin.html', {'all_products': all_products})
    else:
        return render(request, 'user/user_afterlogin.html', {'all_products': all_products, 'user': request.user})


# Admin Functions
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addproduct_view(request):
    if request.method == 'POST':
        form = forms.AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'admin/product_added.html')
    else:
        form = forms.AddProduct()
    return render(request, 'admin/add_product.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if product.image:
        product.image.delete()
    product.delete()
    all_products = Product.objects.all()
    return render(request, 'admin/admin_afterlogin.html', {'all_products': all_products})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    form = forms.AddProduct(instance=product)
    if request.method == 'POST':
        # now this form have data from html
        form = forms.AddProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return render(request, 'admin/product_added.html')
    return render(request, 'admin/add_product.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


def display_product(request, pk):
    if request.method == 'POST':
        print(request.POST)
        print(request.user.id)
        rev = request.POST['rev']
        new_review = Reviews.objects.create(
            product_id=Product.objects.get(id=pk), customer_id=User.objects.get(user_id=request.user.id).id, review=rev)
        new_review.save()
    prod = Product.objects.get(id=pk)
    reviews = Reviews.objects.filter(product_id=pk)
    return render(request, 'user/display_product.html', {'product': prod, 'reviews': reviews})


@login_required(login_url='userlogin')
def view_account(request):
    return render(request, 'user/my_account.html')


@login_required(login_url='userlogin')
def password_template(request):
    return render(request, 'user/change_password.html')


@login_required(login_url='userlogin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = authenticate(username=request.user.username,
                            password=current_password)
        if user is not None:
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(
                    request, 'Your password was successfully updated!')
                return redirect('my_account')
            else:
                messages.error(
                    request, 'The two password fields did not match.')
        else:
            messages.error(request, 'Your current password was incorrect.')
    return render(request, 'user/change_password.html')


def add_to_favorites(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You have to sign in to add to favorites")
        return redirect('../../')
    usr = User.objects.get(user_id=request.user.id)
    print(usr)
    usr.products.add(pk)
    return redirect('../../')


def show_favorites(request):
    if not request.user.is_authenticated:
        messages.error(request, "You have to sign in to show your favorites")
        return redirect('../../')
    user = User.objects.get(user=request.user)
    fav_products = user.products.all()
    return render(request, 'user/favorites.html', {'all_products': fav_products, 'user': request.user})


@login_required(login_url='userlogin')
def remove_favorite(request, pk):
    user = User.objects.get(user=request.user)
    fav_product = user.products.get(id=pk)
    user.products.remove(fav_product)
    user = User.objects.get(user=request.user)
    fav_products = user.products.all()
    return render(request, 'user/favorites.html', {'all_products': fav_products, 'user': request.user})


def add_to_cart(request, pk1):
    if not request.user.is_authenticated:
        messages.error(request, "You have to sign in to add to your cart")
        return redirect('../../../')
    customer = User.objects.get(user=request.user)
    my_cart, created = Cart.objects.get_or_create(customer=customer)
    prod = Product.objects.get(id=pk1)
    my_cart.price += prod.price
    my_cart.save()
    order, bol = OrderedProduct.objects.get_or_create(
        product_id=prod, cart=my_cart, quantity=1)
    order.save()
    messages.success(request, "product is added to the cart successfuly")
    return redirect('../../../')


def remove_from_cart(request, pk):
    customer = User.objects.get(user=request.user)
    prod = OrderedProduct.objects.get(id=pk)
    my_cart = Cart.objects.get(id=prod.cart_id)
    my_cart.price -= prod.product_id.price
    my_cart.save()
    prod.delete()
    return redirect('../../show_cart')


def show_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You have to sign in to show your cart")
        return redirect('../../')
    orders = {}
    cart = object
    usr = User.objects.get(user_id=request.user.id)
    if Cart.objects.filter(customer_id=usr.id).exists():
        cart = Cart.objects.get(customer_id=usr.id)
        orders = OrderedProduct.objects.filter(cart_id=cart.id)
    return render(request, 'user/cart.html', {'orders': orders, 'cart': cart})
