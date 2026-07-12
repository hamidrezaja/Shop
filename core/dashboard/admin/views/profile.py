from django.views.generic import TemplateView,UpdateView
from django.contrib.auth import views as auth_view
from ..forms import AdminProfileEditForm,AdminPasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect 
from django.contrib import messages
from accounts.models import Profile

class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,auth_view.PasswordChangeView):
    template_name='dashboard/admin/profile/security-edit.html'
    form_class=AdminPasswordChangeForm
    success_url=reverse_lazy("dashboard:admin:security-edit")
    #success_message='رمز عبور شما با تغییر کرد .'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'رمز عبور با موفقیت تغییر کرد. لطفاً دوباره وارد شوید.')
        logout(self.request)
        return redirect(reverse_lazy('accounts:login'))
    
class AdminProfileEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    template_name='dashboard/admin/profile/profile-edit.html'
    form_class=AdminProfileEditForm
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = "بروز رسانی پروفایل با موفقیت انجام شد"
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class AdminProfileImageEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    http_method_names=['post']
    model=Profile
    fields=['image']
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = "بروز رسانی پروفایل با موفقیت انجام شد"
    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    def post(self, request, *args, **kwargs):
        
        self.object=self.get_object()        
        if 'delete_image' in request.POST:
            if self.object.image:
                self.object.image.delete(save=False)
                self.object.image="profile/default.png"
                self.object.save()
                messages.success(self.request,'تصویر شما حذف شد ')
                return redirect(self.success_url)
        
        return super().post(request, *args, **kwargs)
    def form_invalid(self, form):
        messages.error(self.request,'آپلود تصویر با انجام نششد لطفا مجدد تلاش کنید')
        return redirect(self.success_url)
    