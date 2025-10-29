
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user.urls')),
    path('employee/',include('employee.urls')),
    path('leave/',include('leave.urls')),
    path('attendance/',include('attendance.urls')),
    path('payroll/',include('payroll.urls')),
    path('customer/',include('customer.urls')),
    path('creditnotes/',include('creditnotes.urls')),
    path('inquiry/',include('inquiry.urls')),
    path('quotation/',include('quotations.urls')),
    path('projects/',include('projects.urls')),
    path('vessels/',include('vessels.urls')),
    path('tasks/',include('tasks.urls')),
    path('requirements/',include('requirements.urls')),
    path('invoices/',include('invoice.urls')),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
