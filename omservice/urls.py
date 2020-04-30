from django.urls import path
from omservice import views
from django.conf.urls import url

urlpatterns = [
    url(r'^page/list/$', views.servicePage, name='servicePage'),
    path('api/save/', views.saveServiceAjax, name='saveServiceAjax'),
    path('api/load/', views.loadServiceAjax, name='loadServiceAjax'),
    path('api/form/', views.getFormListAjax, name='formServiceAjax'),
    path('api/column/', views.getFormObjAjax, name='columnServiceAjax'),
    path('api/request/', views.requestAjax, name='requestServiceAjax'),
    ]