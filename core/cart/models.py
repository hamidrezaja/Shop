from django.db import models
from django.contrib.auth import get_user_model
from store.models import ProductModel
# Create your models here.


User=get_user_model()

class Cart(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
class CartItem(models.Model):
    
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=0)
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    