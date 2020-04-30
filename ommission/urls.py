from django.urls import path
from ommission import views
from django.conf.urls import url

urlpatterns = [
#     url(r'^page/flow-app/$', views.),
    url(r'^page/mission/$', views.mission_page),

    path('api/my-mission/list/', views.listMyMissionAjax, name='listMyMissionAjax'),
    path('api/history-mission/list/', views.listHistoryMissionAjax, name='listHistoryMissionAjax'),
    path('api/history-mission-current-state/list/', views.listHistoryMissionCurrentStateAjax, name='listHistoryMissionCurrentStateAjax'),
    ]