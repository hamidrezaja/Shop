from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,ListView
from .models import ProductModel,ProductStatusType,ProductCategory
from django.core.exceptions import FieldError
# Create your views here.

class ProductsGridView(ListView):
    template_name='store/products-grid.html'
    paginate_by =6
    
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size',self.paginate_by)
    def get_queryset(self):
        queryset=ProductModel.objects.filter(status=ProductStatusType.publish.value)
        if search_q:= self.request.GET.get('q'):
            queryset=queryset.filter(title__icontains =search_q)
        if search_category:=self.request.GET.get('category_id'):
            queryset=queryset.filter(category__id=search_category)
        if min_price:=self.request.GET.get('min_price'):
            queryset=queryset.filter(price__gte=min_price)
        if max_price:=self.request.GET.get('max_price'):
            queryset=queryset.filter(price__lte=max_price)
        if order_by:=self.request.GET.get('order_by'):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['total_items']=self.get_queryset().count()
        context['categories']=ProductCategory.objects.all()
        return context
    
class ProductDetailView(DetailView):
    model = ProductModel    
    template_name='store/product-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
