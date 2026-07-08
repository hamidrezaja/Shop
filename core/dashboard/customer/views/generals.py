from django.views.generic import TemplateView
from dashboard.permissions import HasCustomerAccessPermission

class CustomerDashboardHomeView(HasCustomerAccessPermission,TemplateView):
    template_name='dashboard/customer/home.html'
    