import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import MenuItemsSerializer, CreateOrderSeriailzer, OrderSerializer, MpesaPaymentSerializer, MpesaTransactionSerializer
from .utils import initiate_stk_push
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
            print('item: ', item)
            menu_item = MenuItem.objects.get(id=item.get('item_id'))
            quantity = item.get('quantity')

            OrderItem.objects.create(
               menu_item=menu_item,
               quantity = quantity,
               order=order
            )
         
         serializer = OrderSerializer(order)
         
         return Response(serializer.data, status=201)
   
   def get(self, request, pk):
      queryset = Order.objects.filter(id=pk)
      if queryset.exists():
         order = queryset.first()
         serializer = OrderSerializer(order)
         return Response(serializer.data, status=200)
      else:
         return Response({'message': 'order not found'}, status=404)

class ProcessMpesaPayment(APIView):
   def post(self, request):
      serializer = MpesaPaymentSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         phone_number = serializer.validated_data.get('phone_number')
         order_id = serializer.validated_data.get('order_id')
         order = Order.objects.get(id=order_id)
         amount = order.order_total
         transaction_data = initiate_stk_push(phone_number)
         print('transaction data: ', transaction_data)
         if "errorCode" in transaction_data:
               return Response({
                  "errorCode": transaction_data['errorCode'],
                  "errorMesssage": transaction_data['errorMessage']
               }, status=405)
         else:
               transaction = MpesaTransaction.objects.create(
                  request_id=transaction_data['chechout_request_id'],
                  order=order
               )

               serializer = MpesaTransactionSerializer(transaction)

               return Response(serializer.data, status=201)
         
   def get(self, request, transaction_id):
      queryset = MpesaTransaction.objects.filter(request_id=transaction_id)
      if queryset.exists():
         transaction = queryset.first()
         serializer = MpesaTransactionSerializer(transaction)
         return Response(serializer.data, status=200)
      else:
         return Response({'message': 'Transaction does not exist.'}, status=404)


class MpesaCallback(APIView):
   def post(self, request):
      request_data = json.loads(request.body)
      body = request_data.get("Body")
      result_code = body.get("stkCallback").get("ResultCode")

      if result_code == 0:
         print("Payment successful")
         request_id = body.get("stkCallback").get("CheckoutRequestID")
         metadata = body.get("stkCallback").get("CallbackMetadata").get("Item")

         for data in metadata:
               if data.get("Name") == "MpesaReceiptNumber":
                  receipt_number = data.get("Value")
               elif data.get("Name") == "Amount":
                  amount = data.get("Value")
               elif data.get("Name") == "PhoneNumber":
                  phone_number = data.get("Value")
         print("receipt:", receipt_number)
         print("amouont: ", amount)
         print("request_id: ", request_id)
         transaction = MpesaTransaction.objects.get(request_id=request_id)
         transaction.receipt_number = receipt_number
         transaction.amount = amount
         transaction.phone_number = str(phone_number)
         transaction.is_complete = True
         transaction.save()
         order = transaction.order
         order.paid = True
         order.save()
         return HttpResponse("Ok")