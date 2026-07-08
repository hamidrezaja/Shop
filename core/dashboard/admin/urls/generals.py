from django.urls import path,include
from ..views import generals as views
urlpatterns = [
    path('home/',views.AdminDashboardHomeView.as_view(),name='home')
]
