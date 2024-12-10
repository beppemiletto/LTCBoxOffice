from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.boxoffice, name='boxoffice'),
    path('user_not_allowed/', views.user_not_allowed, name='user_not_allowed'),
    path('event/<int:event_id>/', views.event, name='event'),
    path('boxoffice_cart/<int:event_id>/', views.boxoffice_cart, name='boxoffice_cart'),
    path('boxoffice_plus_price/<int:item_id>/', views.boxoffice_plus_price, name='boxoffice_plus_price'),
    path('boxoffice_minus_price/<int:item_id>/', views.boxoffice_minus_price, name='boxoffice_minus_price'),
    path('boxoffice_remove_cart/<int:item_id>/', views.boxoffice_remove_cart, name='boxoffice_remove_cart'),
    path('boxoffice_cart_cancel/<int:event_id>/', views.boxoffice_cart_cancel, name='boxoffice_cart_cancel'),
    path('boxoffice_print/<int:event_id>/<int:method_id>/', views.boxoffice_print, name='boxoffice_print'),
    path('boxoffice_print/<int:event_id>/<int:method_id>/<int:orderevent_id>/<str:mode_id>/', views.boxoffice_print, name='boxoffice_print'),
    path('close_transaction/<int:event_id>/', views.close_transaction, name='close_transaction'),
    path('change_bookings/<int:event_id>/', views.change_bookings, name='change_bookings'),
    path('customers/<int:event_id>/<str:customer>/', views.customers, name='customers'),
    path('customers/<int:event_id>/', views.customers, name='customers'),
    path('add_bookings/<int:event_id>/<str:customer>/', views.add_bookings, name='add_bookings'),
    path('add_bookings/<int:event_id>/', views.add_bookings, name='add_bookings'),
    path('list_bookings/<int:event_id>/', views.list_bookings, name='list_bookings'),
    path('edit_order/<int:orderevent_id>/', views.edit_order, name='edit_order'),
    # path('box_edit_order/<int:orderevent_id>/', views.box_edit_order, name='box_edit_order'),
    path('edit_booking/<str:boxofficebookingevent_number>/', views.edit_booking, name='edit_booking'),
    path('obliterate/<str:ticket_number>/', views.obliterate, name='obliterate'),
    path('erase_order/<int:userorder_id>/<int:order_id>/', views.erase_order, name='erase_order'),
    path('erase_booking/<int:customerbooking_id>/', views.erase_booking, name='erase_booking'),
    # path('sell_booking/<int:order>/', views.sell_booking, name='sell_booking'),
    path('sell_booking/<int:order>/<str:mode>/', views.sell_booking, name='sell_booking'),
    path('event_list/', views.event_list, name='event_list'),
    path('barcode_read/<int:event_id>', views.barcode_read, name='barcode_read'),
    # path('', views.cart, name='cart'),
    # path('add_cart/<int:event_id>/', views.add_cart, name='add_cart'),
    path('plus_ingresso/<str:number>/<str:seat>/', views.plus_ingresso, name='plus_ingresso'),
    path('plus_ingr_booking/<str:number>/<str:seat>/', views.plus_ingr_booking, name='plus_ingr_booking'),
    path('minus_ingresso/<str:number>/<str:seat>/', views.minus_ingresso, name='minus_ingresso'),
    path('minus_ingr_booking/<str:number>/<str:seat>/', views.minus_ingr_booking, name='minus_ingr_booking'),
    path('remove_seat/<str:number>/<str:seat>/', views.remove_seat, name='remove_seat'),
    path('removeseat_booking/<str:number>/<str:seat>/', views.removeseat_booking, name='removeseat_booking'),
    path('hall_detail/<slug:event_slug>/<str:number>/', views.hall_detail, name='hall_detail'),
    path('send_updatemail/<str:number>/', views.send_updatemail, name='send_updatemail'),
    # path('checkout/', views.checkout, name='checkout'),    
] 