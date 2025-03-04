from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.book_list, name='book_list'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('add/', views.add_book, name='add_book'),
    path('update/<int:book_id>/', views.update_book, name='update_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('cart/', views.view_cart, name='view_cart'),  # Add this line
    path('checkout/', views.checkout, name='checkout'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_money/', views.add_money, name='add_money'),
    
]