from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MpesaTransaction)