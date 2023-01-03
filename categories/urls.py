from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include 
from rest_framework import routers 
from categories import endpoints

from categories import admin
from categories import models 
from . import views 
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from rest_framework.authtoken import views as authtoken_views


router = routers.DefaultRouter() 
router.register(r'orderlines', endpoints.PaidOrderLineViewSet) 
router.register(r'orders', endpoints.PaidOrderViewSet)

urlpatterns = [
    path(
        "contact-us/",
        views.ContactUsView.as_view(),
        name="contact_us",
    ),
   path(
        'signup/', 
        views.SignupView.as_view(), name="signup"),

    path('api/', include(router.urls)),
    #path( "customer-service/<int:order_id>/", views.room, name="cs_chats",),
    #path( "customer-service/", TemplateView.as_view(
            #template_name="customer_service.html" ), name="cs_categories", ),

    path(
        "address/", views.AddressListView.as_view(), name="address_list",
    ), 
    path(
        "address/create/", views.AddressCreateView.as_view(), name="address_create",
    ), 
    path(
        "address/<int:pk>/", views.AddressUpdateView.as_view(), name="address_update",
    ), 
    path(
        "address/<int:pk>/delete/", views.AddressDeleteView.as_view(), name="address_delete",
),
    path('my-order/', views.my_order_view,name='my-order'),
    path(
         "order-dashboard/", views.OrderView.as_view(), name="order_dashboard",
),

    path(
        "order/done/",
        TemplateView.as_view(template_name="order_done.html"),
        name="checkout_done",
    ),
    path(
        "order/address_select/",
        views.AddressSelectionView.as_view(),
        name="address_select",
    ),
    path(
        "add_to_basket/", views.add_to_basket, name="add_to_basket" ),

    path('basket/', views.manage_basket, name="basket"),

    path('search/', views.products, name="search_products"),

    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/category/<slug:category>/', TemplateView.as_view(), name='category_show'),
    path('brands/<slug:slug>/', views.brand, name='brand'),

    path('brands/apple/', views.brand_apple, name='brand_apple'),
    path('brands/hp/', views.brand_hp, name='brand_hp'),
    path('brands/dell/', views.brand_dell, name='brand_dell'),
    path('brands/asus/', views.brand_asus, name='brand_asus'),
    path('brands/samsung/', views.brand_samsung, name='brand_samsung'),
    path('brands/lenovo/', views.brand_lenovo, name='brand_lenovo'),
    path('brands/toshiba/', views.brand_toshiba, name='brand_toshiba'),


    path('brands/programminglaptops/', views.brand_programminglaptops, name='brand_programminglaptops'),

    path('brands/businesslaptops/', views.brand_businesslaptops, name='brand_businesslaptops'),

    #path('room/<int:id>/<slug:slug>/', views.product_chat_room, name='product_chat_room'),
#path( "customer-service/<int:order_id>/", views.room, name="cs_chats",),

    path('category/<slug:category>/', views.ProductListView.as_view(), name='product_list_category'),
    path('bestseller/', views.product_bestseller, name='product_bestseller'),
    #path('flashsales/', views.product_flashsales, name='product_flashsales'),
    path('bestdeals/', views.product_bestdeals, name='product_bestdeals'),
    #path('featured/', views.product_featured, name='product_featured'),
    #path('toppicksforyou/', views.product_toppicksforyou, name='product_toppicksforyou'),
    

    #path('<uuid:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path(
        "mobile-api/auth/", 
        authtoken_views.obtain_auth_token, 
        name="mobile_token",
),

    path( "mobile-api/my-orders/", 
    endpoints.my_orders, 
    name="mobile_my_orders",
),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


#33pastebin