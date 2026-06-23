from django.urls import path,re_path
from . import views
app_name='store'
urlpatterns = [
    path('products-grid/',views.ProductsGridView.as_view(),name='products-grid'),
    re_path(r'(?P<slug>[-\w]+)/detail/',views.ProductDetailView.as_view(),name='product-detail'),
    
]
