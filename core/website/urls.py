from django.urls import path
from . import views
app_name='website'
urlpatterns = [
    path("",views.Index_view.as_view(),name='index'),
    path("contact/",views.Contact_view.as_view(),name='contact'),
    path("about/",views.About_view.as_view(),name='about'),

]
