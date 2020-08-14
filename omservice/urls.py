from django.urls import path
from omservice import views
from django.conf.urls import url

urlpatterns = [
    url(r'^page/list/$', views.servicePage, name='servicePage'),
    path('api/save/', views.saveServiceAjax, name='saveServiceAjax'),
    path('api/load/', views.loadServiceAjax, name='loadServiceAjax'),
    path('api/form/', views.getFormListAjax, name='getFormListAjax'),
    path('api/column/', views.getFormObjAjax, name='getFormObjAjax'),
    path('api/request/', views.requestAjax, name='requestAjax'),
    path('api/import/', views.importTranslationAjax, name='importTranslationAjax'),
    path('api/export/', views.exportTranslationAjax, name='exportTranslationAjax'),
    path('api/exportall/', views.exportServcieAjax, name='exportServcieAjax'),
    path('api/subqueryH/', views.SubQueryHeaderAjax, name='SubQueryHeaderAjax'),
    path('api/subqueryD/', views.SubQueryDataAjax, name='SubQueryDataAjax'),
    ]