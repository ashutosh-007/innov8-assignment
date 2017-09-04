from django.conf.urls import url, include
from django.contrib import admin

from . import views
from . import forms
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/register/', views.signup_with_email_verification, name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^auth/login/$', auth_views.login,{'template_name':'login.html','authentication_form':forms.LoginForm}, name='login'),
    url(r'^auth/logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^auth/account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^auth/change_password/$', views.change_password, name='change_password'),
    url(r'^auth/view_profile/(?P<user_id>[0-9]+)/$', views.view_profile, name='view_profile'),
    url(r'^auth/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                         views.activate, name='activate'),
]
