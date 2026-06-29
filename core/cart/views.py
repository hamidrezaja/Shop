from django.shortcuts import render,redirect
from django.views.generic import View
from .cart import CartSession
from store.models import ProductModel
from django.shortcuts import get_object_or_404
# Create your views here.
class AddCartView(View):
    def post(self,request,product_id):
        cart=CartSession(request.session)
        product=get_object_or_404(ProductModel,id=product_id)
        cart.add_cart(product=product)
        return redirect(request.META.get('HTTP_REFERER'))
    
class DetailCartView(View):
    def get(self,request):
        cart=CartSession(request.session)
        obj=cart.get_cart_items()
        total_price=cart.get_total_price()
        return  render(request,'cart/detail_cart.html',{'cart':obj,'total_price':total_price})

class RemoveCartView(View):
    def post(self,request,product_id):
        cart=CartSession(request.session)
        product=get_object_or_404(ProductModel,id=product_id)
        cart.remove_cart(product)
        return redirect('cart:detail-cart')
    
class UpdateCartView(View):
    def post(self, request, product_id):
        cart = CartSession(request.session)
        product = get_object_or_404(ProductModel, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart.update_cart(product, quantity)
        return redirect(request.META.get('HTTP_REFERER'))
    