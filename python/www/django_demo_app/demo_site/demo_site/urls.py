"""demo_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path

from demo_site import auth, tenant
from demo_site import scan

urlpatterns = [
    path('login', auth.LoginApi.as_view()),
    path('logout', auth.LogoutApi.as_view()),
    path('renew', auth.RenewApi.as_view()),
    path('currentUser',auth.currentUserApi.as_view()),
    path('register', tenant.RegisterApi.as_view()),
    path('job', scan.ScanServiceApi.as_view()),
    path('getScanById/<job_id>', scan.ScanDetailsApi.as_view()),
    path('getScanResult', scan.ScanResultApi.as_view()),
    path('getScanJobs', scan.ScanListApi.as_view()),
    path('sendEmail', scan.ScanEmailApi.as_view()),
    path('deleteJob/<job_id>', scan.removeJobApi.as_view()),
    path('getTenantById/<tenantId>',tenant.TenantApi.as_view()),
    path('deleteTenantById/<tenantId>',tenant.DeleteTenantApi.as_view())
    
    # re_path(r'^admin/', admin.site.urls),
]
