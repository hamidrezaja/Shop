from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from accounts.models import UserType




class HasAdminAccessPermission( UserPassesTestMixin):
    
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.admin.value
        return False
    
    
class HasCustomerAccessPermission(UserPassesTestMixin):
    
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.customer.value
        return False