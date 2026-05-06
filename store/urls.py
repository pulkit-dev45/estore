from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('category/<int:id>/', views.category_filter, name='category'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:id>/', views.remove_cart, name='remove'),
    path('increase/<int:id>/', views.increase_qty, name='increase'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('contact/', views.contact_view, name='contact'),
    path('terms/', views.term_view, name='term'),
    path('privacy', views.privacy_view, name='privacy'),
   




    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),


]
