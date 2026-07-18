from django.contrib import admin
from .models import CartItem,Cart
# Register your models here.

@admin.register(CartItem)   
class CartItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)   
class CartAdmin(admin.ModelAdmin):
    pass

