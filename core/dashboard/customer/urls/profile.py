from django.urls import path,include
from .. import views
urlpatterns = [
    path('security/edit/',views.CustomerSecurityEditView.as_view(),name='security-edit'),
    path('profile/edit/',views.CustomerProfileEditView.as_view(),name='profile-edit'),
    
]
