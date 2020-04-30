from django.urls import path
from omdashboard import views
from django.conf.urls import url

urlpatterns = [
    path('api/save/', views.saveDashboardAjax, name='saveDashboardAjax'),
    path('api/load/', views.loadDashboardAjax, name='loadDashboardAjax'),
    path('api/update/', views.updateGridAjax, name='updateGridAjax'),
    path('api/form/', views.getFormListAjax, name='formGridAjax'),
    path('api/model/', views.getColumnListAjax, name='columnGridAjax'),
    ]