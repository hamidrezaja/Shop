from django.views.generic import TemplateView
from dashboard.permissions import HasAdminAccessPermission

class AdminDashboardHomeView(HasAdminAccessPermission,TemplateView):
    template_name='dashboard/admin/home.html'