"""Supermarket_SS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from supermarket_app import views
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static

urlpatterns = [

    # Home Page Link
    path('', views.home_view, name='product_search_home'),
    path('admin/', admin.site.urls),
    path('sortbyname', views.sortbyname),
    path('sortbyprice', views.sortbyprice),
    path('new_arrivals', views.new_arrivals),

    # # Registration Links
    # path('adminsignup', views.adminsignup_view),
    path('signup', views.usersignup_view),
    # path('adminlogin', LoginView.as_view(
    #     template_name='regist/adminlogin.html')),
    path('userlogin', LoginView.as_view(template_name='regist/userlogin.html')),

    # After Login Link
    path('afterlogin', views.afterlogin_view),

    # Admin Links
    path('addproduct', views.addproduct_view),
    path('success', views.success, name='success'),
    path('delete_product/<str:pk>/', views.delete_product, name='delete'),
    path('edit_product/<str:pk>/', views.edit_product, name='edit'),
    # path('viewusers', views.view_users),
    # path('contact', views.contactusers),

    # User Links
    path('display_product/<str:pk>/',
         views.display_product, name='display'),
    path('add_favorite/<int:pk>/', views.add_to_favorites, name='add_fav'),
    path('show_favorites', views.show_favorites),
    path('remove_favorite/<int:pk>/',
         views.remove_favorite, name='remove_favorite'),
    path('add_to_cart/<pk1>/',
         views.add_to_cart, name="add"),
    path('remove_from_cart/<int:pk>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('show_cart', views.show_cart),
    path('my_account', views.view_account),
    path('change_password', views.password_template),

    # Logout Link
    path('logout', LogoutView.as_view(next_page='/')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
