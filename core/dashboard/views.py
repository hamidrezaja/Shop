from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserType
from django.urls import reverse_lazy
# Create your views here.



class DashboardHomeView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            if self.request.user.type == UserType.admin.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
            if self.request.user.type == UserType.customer.value:
                return redirect(reverse_lazy('dashboard:customer:home'))
        else:
            return redirect(reverse_lazy('accounts:login'))
        
        return super().dispatch(request, *args, **kwargs)