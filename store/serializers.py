from rest_framework import serializers
from .models import MenuItem, Customer, Order, MpesaTransaction

class MenuItemsSerializer(serializers.ModelSerializer):
   class Meta:
      model = MenuItem
      fields = "__all__"
   
class CreateOrderItemSerializer(serializers.Serializer):
   item_id = serializers.IntegerField()
   quantity = serializers.IntegerField()

class CustomerSerializer(serializers.ModelSerializer):
   class Meta:
      model = Customer
      fields = "__all__"

class CreateOrderSeriailzer(serializers.Serializer):
   order_items = CreateOrderItemSerializer(many=True)
   customer = CustomerSerializer()

class OrderSerializer(serializers.ModelSerializer):
   customer = CustomerSerializer()
   class Meta:
      model = Order
      fields = '__all__'
   
class MpesaPaymentSerializer(serializers.Serializer):
   phone_number = serializers.IntegerField()
   order_id = serializers.IntegerField()

class MpesaTransactionSerializer(serializers.ModelSerializer):
   class Meta:
      model = MpesaTransaction
      fields = "__all__"