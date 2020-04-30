from django.urls import path
from ommessage import views
from django.conf.urls import url

urlpatterns = [
    url(r'^page/messageManage/(?P<url>.+)$', views.message_index),
    url(r'^page/compose/(\w*)\/*$', views.message_compose),
    
    path('api/messages/list/', views.listMessagesAjax, name='listMessagesAjax'),
    path('api/message-history/list/', views.listMessageHistoryAjax, name='listMessageHistoryAjax'),
    path('api/messages/create/', views.createMessagesAjax, name='createMessagesAjax'),
    path('api/message-history/load/', views.loadMessageHistoryAjax, name='loadMessageHistoryAjax'),
    path('api/message-history/create/', views.createMessageHistoryAjax, name='createMessageHistoryAjax'),
    path('api/message-detail/compose/', views.composeMessageDetailAjax, name='composeMessageDetailAjax'),
    path('api/message-history/delete/', views.deleteMessageHistoryAjax, name='deleteMessageHistoryAjax'),
    path('api/send-user/search/', views.searchSendUserAjax, name='searchSendUserAjax'),
    path('api/send-group/search/', views.searchSendGroupAjax, name='searchSendGroupAjax'),
    path('api/send-group-user/search/', views.searchGroupUserAjax, name='searchGroupUserAjax'),
]