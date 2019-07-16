from django.contrib import admin
from django.urls import path, include # new
from django.views.generic.base import TemplateView # new
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('currency/', include('currency.urls')),
    path('', TemplateView.as_view(template_name='home.html'), 	name='home'),
    path('login/',views.user_login, name='login'),

    path('', include('django.contrib.auth.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



"""
urlpatterns += [
    path('currency/', include('currency.urls')),
]
"""
