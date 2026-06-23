from django.contrib import admin
from .models import ProductModel,ProductCategory,ProductImageModel
# Register your models here

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id","title", "stock","created_date")

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id","title","created_date")
    
@admin.register(ProductImageModel)   
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id","file","created_date")








