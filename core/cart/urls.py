from django.urls import path,re_path
from . import views
app_name='cart'
urlpatterns = [
    path('add-cart/<product_id>',views.AddCartView.as_view(),name='add-cart'),
    path('detail-cart/',views.DetailCartView.as_view(),name='detail-cart'),
    path('remove-cart/<int:product_id>',views.RemoveCartView.as_view(),name='remove-cart'),
    path('update-cart/<int:product_id>/', views.UpdateCartView.as_view(), name='update-cart'),
    
]
