
from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('error/', views.error, name='error'),
    path('cart/', views.cart, name='cart'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart_remove/<int:id>/', views.add_to_cart_remove, name='add_to_cart_remove'),
    path('increment/<int:id>/', views.increment, name='increment'),
    path('decrement/<int:id>/', views.decrement, name='decrement'),
    path('Wish_list/', views.Wish_list, name='Wish_list'),
    path('add_to_Wishlist/<int:id>/', views.add_to_Wishlist, name='add_to_Wishlist'),
    path('remove_Wishlist/<int:id>/', views.remove_Wishlist, name='remove_Wishlist'),
    path('chackout/', views.chackout, name='chackout'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('log_out/', views.log_out, name='log_out'),
    path('register/', views.register, name='register'),
    path('forgot/', views.forgot, name='forgot'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('shop_detail/<int:id>/', views.shop_detail, name='shop_detail'),
    path('fack_detail', views.fack_detail, name='fack_detail'),
    path('shop/', views.shop, name='shop'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('Price_filter', views.Price_filter, name='Price_filter'),
    path('Search_filter', views.Search_filter, name='Search_filter'),
    path('Related_products', views.Related_products, name='Related_products')



]