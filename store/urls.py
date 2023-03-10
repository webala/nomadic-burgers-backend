from django.urls import path
from .views import *

urlpatterns = [
   path('menuitems', MenuItemsView.as_view(), name='menu-items'),
   path('menuitem/<int:pk>', MenuItemView.as_view(), name='menu-item'),
   path('order', OrderView.as_view(), name='order'),
   path('ordercomplete', set_order_complete, name='set-order-complete'),
   path('orders', OrdersListView.as_view(), name='orders'),
   path('orderitems/<int:order_id>', order_items, name='order-items'),
   path('order/<int:pk>', OrderView.as_view(), name='order-detail'),
   path('payment', ProcessMpesaPayment.as_view(), name='mpesa-payment'),
   path('mpesacallback', MpesaCallback.as_view(), name='mpesa-payment'),
   path('transaction/<transaction_id>', ProcessMpesaPayment.as_view(), name='mpesa-transaction'),  
]