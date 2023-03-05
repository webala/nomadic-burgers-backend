from django.urls import path
from .views import *

urlpatterns = [
   path('menuitems', MenuItemsView.as_view(), name='menu-items'),
   path('menuitem/<int:pk>', MenuItemView.as_view(), name='menu-item'),
   path('order', OrderView.as_view(), name='order'),
   path('order/<int:pk>', OrderView.as_view(), name='order-detail'),
   path('payment', ProcessMpesaPayment.as_view(), name='mpesa-payment'),
   path('mpesacallback', MpesaCallback.as_view(), name='mpesa-payment'),
   path('transaction/<transaction_id>', ProcessMpesaPayment.as_view(), name='mpesa-transaction'),  
]