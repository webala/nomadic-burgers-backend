from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import MenuItemsSerializer, CreateOrderSeriailzer, OrderSerializer
# Create your views here.


class MenuItemsView(generics.ListAPIView):
   model = MenuItem
   queryset = MenuItem.objects.all()
   serializer_class = MenuItemsSerializer

class MenuItemView(generics.RetrieveAPIView):
   model = MenuItem
   queryset = MenuItem.objects.all()
   serializer_class = MenuItemsSerializer

class OrderView(APIView):
   def post(self, request):
      seriallizer = CreateOrderSeriailzer(data=request.data)
      if seriallizer.is_valid(raise_exception=True):
         data = seriallizer.validated_data
         customer_data = data.get('customer')
         order_items_data = data.get('order_items')

         customer = Customer.objects.create(
            phone_number = customer_data.get('phone_number'),
            name = customer_data.get('name')
         )

         order = Order.objects.create(customer=customer)

         for item in order_items_data:
            menu_item = MenuItem.objects.get(id=item.get('id'))
            quantity = item.get('quantity')

            OrderItem.objects.create(
               menu_item=menu_item,
               quantity = quantity,
               order=order
            )
         
         serializer = OrderSerializer(order)
         
         return Response(serializer.data, status=201)
         
