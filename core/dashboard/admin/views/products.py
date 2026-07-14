from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView
from store.models import ProductModel,ProductCategory,ProductImageModel
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin 
from ..forms.products import CreateProductForm , ProductImageForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect 
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404

class ProductListAdminView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    
    template_name='dashboard/admin/products/products-list.html'
    paginate_by=10
    
    def get_queryset(self):
        queryset=ProductModel.objects.all()
        if category_filter := self.request.GET.get('category_id'):
            queryset=queryset.filter(category__id=category_filter)
        if product_search := self.request.GET.get('product_search'):
            queryset=queryset.filter(title__icontains=product_search)
        if product_order := self.request.GET.get('product_order'):
            queryset=queryset.order_by(product_order)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        
        context=super().get_context_data(**kwargs)
        context['categories']=ProductCategory.objects.all()
        context['total_products']=self.get_queryset().count()
        
        return context
    
class CreateProductAdminView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,CreateView):
    
    template_name='dashboard/admin/products/create-product.html'
    queryset=ProductModel.objects.all()
    form_class=CreateProductForm
    success_message = "ایجاد محصول با موفقیت انجام شد"
    success_url=reverse_lazy('dashboard:admin:product-list')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    
class AdminProductEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    
    template_name='dashboard/admin/products/edit-product.html'
    queryset=ProductModel.objects.all()
    form_class=CreateProductForm
    success_message = "ویرایش محصول با موفقیت انجام شد"
    success_url=reverse_lazy('dashboard:admin:product-list')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['image_form']=ProductImageForm()
        return context
    
class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin,DeleteView):
    
    model=ProductModel
    template_name='dashboard/admin/products/delete-product.html'
    success_message='محصول با موفقیت حذف شد'
    success_url=reverse_lazy('dashboard:admin:product-list')
    
    
class AddProductImageAdminView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,CreateView):
    
    model=ProductImageModel
    form_class=ProductImageForm
    http_method_names=['post']
    success_message='تصویر به محصول اضافه شد '
    
    def form_valid(self, form):
        product=get_object_or_404(ProductModel,pk=self.kwargs['pk'])
        form.instance.product=product
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'مشکلی در ارسال تصویر پیش آمده لطفا مجدد تلاش کنید')
        return redirect(reverse_lazy('dashboard:admin:edit-product',kwargs={'pk':self.kwargs.get('pk')}))
        
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:edit-product',kwargs={'pk':self.kwargs.get('pk')})
    
    
class DeleteProductImageAdminView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin,DeleteView):
    model=ProductImageModel
    http_method_names=['post']
    success_message='تصویر حذف شد '
    
    def get_queryset(self):
        return ProductImageModel.objects.filter(product__pk=self.kwargs['pk'])
    def get_object(self, queryset =None):
        return self.get_queryset().get(pk=self.kwargs['image_pk'])

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:edit-product',kwargs={'pk':self.kwargs.get('pk')})
    def form_valid(self, form):
        image = self.object
        if image.file:
            image.file.delete(save=False)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'مشکلی در حذف تصویر پیش آمده لطفا مجدد تلاش کنید')
        return redirect(reverse_lazy('dashboard:admin:edit-product',kwargs={'pk':self.kwargs.get('pk')}))