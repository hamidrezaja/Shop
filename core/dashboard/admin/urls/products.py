from django.urls import path,include
from .. import views
urlpatterns = [
    path('product/list/',views.ProductListAdminView.as_view(),name='product-list'),
    path('product/create/',views.CreateProductAdminView.as_view(),name='create-product'),
    path('product/edit/<int:pk>/',views.AdminProductEditView.as_view(),name='edit-product'),
    path('product/delete/<int:pk>/',views.AdminProductDeleteView.as_view(),name='delete-product'),
    path('product/add-image/<int:pk>/',views.AddProductImageAdminView.as_view(),name='add-image-product'),
    path('product/<int:pk>/delete-image/<int:image_pk>/',views.DeleteProductImageAdminView.as_view(),name='delete-image-product'),
       
]
