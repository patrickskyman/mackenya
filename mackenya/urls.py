"""mackenya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from categories import views
from categories.views import ProductListView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from categories import forms
from categories import admin

urlpatterns = [
    path('admin/', admin.categories_admin.urls),
    path("office-admin/", admin.central_office_admin.urls),
    path("dispatch-admin/", admin.dispatchers_admin.urls),
    
    path(
        "order-dashboard/", views.OrderView.as_view(), name="order_dashboard",
),
    path(
        "contact-us/",
        views.ContactUsView.as_view(),
        name="contact_us",
    ),

    path(
        'signup/', 
        views.SignupView.as_view(), name="signup"),
   path(
        "login/", auth_views.LoginView.as_view( template_name="login.html",
        form_class=forms.AuthenticationForm, ),
        name="login",
), 
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api-auth/', include('rest_framework.urls')),
    #path('cart/', include('cart.urls', namespace='cart')),
    #path('orders/', include('orders.urls', namespace='orders')),
    #path('payment/', include('payment.urls', namespace='payment')),
    path('product/', include('categories.urls', )),
    #path('marketing/', include('carousel.urls', namespace='carousel')),
    ##path('search', include('search.urls', namespace='search')),
    #path('', ProductListView.as_view(), name='product_list'),
    path('', views.index, name='index'),
    #path('', views.home, name='home'),
    #path('', TemplateView.as_view(template_name="other/carousel.html")),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
  

   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#handler404 = 'mackenya.views.file_not_found_404'