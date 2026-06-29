from store.models import ProductModel

class CartSession:
    
    def __init__(self,session):
        self.session=session
        self.cart=self.session.setdefault("cart",{})
    
    def add_cart(self,product,quantity=1):
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
            'quantity': quantity,
        }
        else:
            self.cart[product_id]['quantity']+=quantity
        self.save()
    def remove_cart(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()   
    def update_cart(self,product,quantity):
        product_id=str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity']=quantity
            self.save()
            
    def save(self):
        self.session.modified = True
        
    def get_cart_items(self):
        cart_items=[]
        product_ids=self.cart.keys()
        products=ProductModel.objects.filter(id__in=product_ids)
        for product in products:
            product_price=product.get_price()
            
            cart_items.append({
                'product':product,
                'quantity':self.cart[str(product.id)]['quantity'],
                'total_price':product_price*(self.cart[str(product.id)]['quantity'])
            })
        return cart_items
    def get_total_price(self):
        total_price=0
        cart_items=self.get_cart_items()
        for item in cart_items:
            total_price+=item['total_price']
        return total_price + round(total_price * 9 / 100)
    def get_cart_dict(self):
        return self.cart
    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True
    def __len__(self):
        return len(self.cart)
            