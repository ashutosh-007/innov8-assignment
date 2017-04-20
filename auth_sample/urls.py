from django.conf.urls import url
from django.contrib import admin

from . import views
from . import forms
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.signup_with_email_verification, name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', auth_views.login,{'template_name':'login.html','authentication_form':forms.LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                         views.activate, name='activate'),
]
