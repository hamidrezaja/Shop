from django.db import models
from decimal import Decimal
from django.utils.text import slugify
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.


class ProductStatusType(models.IntegerChoices):
    publish=1,('فعال')
    draft=2,('غیرفعال')

class ProductCategory(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(allow_unicode=True,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class ProductModel(models.Model):
    user=models.ForeignKey('accounts.CustomUser',on_delete=models.PROTECT)
    category=models.ManyToManyField(ProductCategory)
    title=models.CharField(max_length=255)
    slug=models.SlugField(allow_unicode=True,unique=True)
    image=models.ImageField(default='default/product-img.png',upload_to='product/img/')
    description=models.TextField()
    brief_description=models.TextField(null=True,blank=True)
    stock=models.PositiveIntegerField(default=0)
    status=models.IntegerField(choices=ProductStatusType.choices,default=ProductStatusType.draft.value)
    price=models.DecimalField(default=0,max_digits=10,decimal_places=0)
    discount_percent=models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-created_date']
    
    def get_price(self):
        discount_price= self.price * Decimal(self.discount_percent / 100)
        discounted_price= self.price - discount_price
        return  round(discounted_price)
    def is_discounted(self):
        return self.discount_percent != 0
    def is_published(self):
        return self.status == ProductStatusType.publish.value
class ProductImageModel(models.Model):
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    file=models.ImageField(upload_to='product/extra-img/')
    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    
    
