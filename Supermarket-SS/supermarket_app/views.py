from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product
from . import forms

# Home Page functions


def home_view(request):
    all_products = Product.objects.all()
    if request.method == 'POST':
        form = forms.ProductForm()
        if form.is_valid:
            if request.POST.get('searchby') == 'product_name':
                all_products = Product.objects.filter(
                    product_name=request.POST.get('search-result'))
            elif request.POST.get('searchby') == 'product_category':
                all_products = Product.objects.filter(
                    product_category=request.POST.get('search-result'))

    return render(request, 'home/index.html', {'all_products': all_products})


def sortbyname(request):
    all_products = Product.objects.all().order_by('product_name')
    return render(request, 'home/index.html', {'all_products': all_products})


def sortbyprice(request):
    all_products = Product.objects.all().order_by('price')
    return render(request, 'home/index.html', {'all_products': all_products})

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
        return HttpResponseRedirect('userlogin')
    return render(request, 'regist/usersignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# After Login function
def afterlogin_view(request):
    all_products = Product.objects.all()
    print(is_admin(request.user))
    if is_admin(request.user):
        return render(request, 'admin/admin_afterlogin.html', {'all_products': all_products})
    else:
        return render(request, 'user/user_afterlogin.html', {'all_products': all_products})


# Admin Functions
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addproduct_view(request):

    if request.method == 'POST':
        form = forms.AddProduct(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = forms.AddProduct()
    return render(request, 'admin/add_product.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_product(request, pk):
    return render(request, 'library/admin/adminafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_product(request, pk):
    return render(request, 'library/admin/addbook.html')


def success(request):
    return HttpResponse('successfully uploaded')
