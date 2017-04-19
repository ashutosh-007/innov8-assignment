import django.conf.urls
from django.contrib import admin

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    django.conf.urls.url(r'^admin/', admin.site.urls),
    django.conf.urls.url(r'^signup/$', views.signup, name ='signup'),
    django.conf.urls.url(r'^register/', views.signup_with_email_verification, name ='register'),
    django.conf.urls.url(r'^home/$', views.home, name ='home'),
    django.conf.urls.url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    django.conf.urls.url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    django.conf.urls.url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    django.conf.urls.url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                         views.activate, name='activate'),
]
