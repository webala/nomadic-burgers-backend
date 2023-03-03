from django.urls import path
from .views import *

urlpatterns = [
   path('menuitems', MenuItemsView.as_view(), name='menu-items'),
   path('menuitem/<int:pk>', MenuItemView.as_view(), name='menu-item'),
   path('order', OrderView.as_view(), name='order'),
]