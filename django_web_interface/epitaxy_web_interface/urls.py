# -*- coding: utf-8 -*-
from core import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'epitaxy_web_interface'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_files/', views.upload_files, name='upload_files'),
    path('predict/', views.predict, name='predict'),
    path('end/<int:code>/', views.end, name='end'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
