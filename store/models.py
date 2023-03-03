from django.db import models

# Create your models here.
 
class Menu(models.Model):
   menu_type = models.CharField(max_length=20)


class MenuItem(models.Model):
   name = models.CharField(max_length=20)
   price = models.DecimalField(max_digits=7, decimal_places=2)
   available = models.BooleanField(default=True)
   menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

class Customer(models.Model):
   phone_number = models.CharField(max_length=13)
   name = models.CharField(max_length=20)

class Order(models.Model):
   customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
   date = models.DateTimeField(auto_now_add=True)
   complete = models.BooleanField(default=False)
   paid = models.BooleanField(default=False)

   @property
   def menu_items(self):
      items = self.orderitem_set.all()
      return sum([item.quantity for item in items])
   
   @property
   def order_total(self):
      items = self.orderitem_set.all()
      return sum([item.item_total for item in items])


class OrderItem(models.Model):
   menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
   quantity = models.IntegerField()
   order = models.ForeignKey(Order, on_delete=models.CASCADE)

   @property
   def item_total(self):
      return self.quantity * self.menu_item.price


class MpesaTransaction(models.Model):
    request_id = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    is_complete = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    receipt_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.receipt_number if self.receipt_number else self.request_id