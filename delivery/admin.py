from django.contrib import admin
from .models import Delivery, DeliveryPerson

# Register your models here.
admin.site.register(Delivery)
admin.site.register(DeliveryPerson)