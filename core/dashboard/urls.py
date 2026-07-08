from django.urls import path,include
from . import views
app_name='dashboard'
urlpatterns = [
    path('admin/',include('dashboard.admin.urls')),
    path('customer/',include('dashboard.customer.urls')),
    path('home/',views.DashboardHomeView.as_view(),name='home'),
    

]
