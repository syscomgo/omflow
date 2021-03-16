from django.urls import path
from omorganization import views
from django.conf.urls import url

urlpatterns = [
    url(r'^page/organization-management/$', views.organizationPage),
    url(r'^page/position-management/$', views.positionPage),
    
    path('api/organization/load/', views.loadOrganizationAjax, name='loadOrganizationAjax'),
    path('api/organization/update/', views.updateOrganizationAjax, name='updateOrganizationAjax'),
    path('api/position/create/', views.createPositionAjax, name='createPositionAjax'),
    path('api/position/update/', views.updatePositionAjax, name='updatePositionAjax'),
    path('api/position/delete/', views.deletePositionAjax, name='deletePositionAjax'),
    path('api/position/list/', views.listPositionAjax, name='listPositionAjax'),
]