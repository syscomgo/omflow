from django.urls import path
from ommonitor import views
from django.conf.urls import url

urlpatterns = [
    url(r'^page/monitorManagePage/$', views.monitorManagePage),
    url(r'^page/monitorDesignPage/(?P<url>.+)$', views.monitorDesignPage),
    url(r'^page/monitorAPIManagePage/$', views.monitorAPIManagePage),
    url(r'^page/monitorAPIDesignPage/(?P<url>.+)$', views.monitorAPIDesignPage),
    url(r'^page/nodeGroupsManagePage/$', views.nodeGroupsManagePage),
    url(r'^page/nodeListManagePage/(?P<url>.+)$', views.nodeListManagePage),
    url(r'^page/nodeManagePage/(?P<url>.+)$', views.nodeManagePage),
    url(r'^page/parameterPage/(?P<url>.+)$', views.monitorParameterPage),
    url(r'^page/eventManagePage/$', views.eventManagePage),
#     url(r'^page/workflowManagePage/(?P<url>.+)$', views.workflowManagePage),
#     url(r'^page/scheduleflowManagePage/$', views.scheduleflowManagePage),
#     url(r'^page/flowCreatePage/$', views.flowCreatePage),
#     url(r'^page/flowDesignPage/(?P<url>.+)$', views.flowDesignPage),
#     url(r'^page/workflowPage/(?P<url>.+)$', views.workflowPage),
#     url(r'^page/flowvaluePage/(?P<url>.+)$', views.flowvaluePage),
    
    #node管理
    path('api/monitor-node/edit/', views.editCollectorAjax, name='editCollectorAjax'),
    path('api/monitor-node/delete/', views.deleteCollectorAjax, name='deleteCollectorAjax'),
    path('api/monitor-node/group/', views.groupCollectorAjax, name='groupCollectorAjax'),
    path('api/monitor-node/list/', views.listCollectorAjax, name='listCollectorAjax'),
    path('api/monitor-node/load/', views.loadCollectorAjax, name='loadCollectorAjax'),
    path('api/monitor-node-policys/load/', views.listNodePolicysAjax, name='listNodePolicysAjax'),
    
    
    
    #policy管理
    path('api/monitor-app/export/', views.exportMonitorApplicationAjax, name='exportMonitorApplicationAjax'),
    path('api/monitor-app/import/', views.importMonitorApplicationAjax, name='importMonitorApplicationAjax'),
    path('api/monitor-flow/create/', views.createMonitorFlowAjax, name='createMonitorFlowAjax'),
    path('api/monitor-flow/list/', views.listMonitorFlowAjax, name='listMonitorFlowAjax'),
    path('api/monitor-flow/update/', views.updateMonitorFlowAjax, name='updateMonitorFlowAjax'),
    path('api/monitor-flow/load/', views.loadMonitorFlowAjax, name='loadMonitorFlowAjax'),
    path('api/monitor-flow/delete/', views.deleteMonitorFlowAjax, name='deleteMonitorFlowAjax'),
    path('api/monitor-flow/copy/', views.copyMonitorFlowAjax, name='copyMonitorFlowAjax'),
    path('api/monitor-flow-outside/get/', views.getOutsideFlowAjax, name='getMonitorOutsideFlowAjax'),
    path('api/monitor-flow-version/list/', views.listMonitorFlowVersionAjax, name='listMonitorFlowVersionAjax'),
    path('api/monitor-flow-version/load/', views.loadMonitorFlowVersionAjax, name='loadMonitorFlowVersionAjax'),
    path('api/monitor-flow-version/delete/', views.deleteMonitorFlowVersionAjax, name='deleteMonitorFlowVersionAjax'),
    #自訂應用-取得流程api格式
    path('api/monitor-flow-api-format/get/', views.getMonitorFlowAPIFormatAjax, name='getMonitorFlowAPIFormatAjax'),
    
    #派送流程至node
    path('api/monitor-flow/dispatch/', views.dispatchMonitorFlowAjax, name='dispatchMonitorFlowAjax'),
    path('api/monitor-flow/remove/', views.removePolicyCollectorAjax, name='removePolicyCollectorAjax'),
    
    #監控項目回傳資料建立、查詢相關
    path('api/policy-data/create/', views.createPolicyDataAjax, name='createPolicyDataAjax'),
    path('api/policy-data/list/', views.listPolicyDataAjax, name='listPolicyDataAjax'),
    path('api/policy-node/lod/', views.loadPolicyCollectorsAjax, name='loadPolicyCollectorsAjax'),
    
    #分散運算
    path('api/python-result/receive/', views.receivePythonResultAjax, name='receivePythonResultAjax'),
    path('api/python/receive/', views.receivePythonAjax, name='receivePythonAjax'),
    
    #收集器群組
    path('api/node-group/create/', views.createCollectorGroupAjax, name='createCollectorGroupAjax'),
    path('api/node-group/list/', views.listCollectorGroupAjax, name='listCollectorGroupAjax'),
    path('api/node-group/update/', views.updateCollectorGroupAjax, name='updateCollectorGroupAjax'),
    path('api/node-group/delete/', views.deleteCollectorGroupAjax, name='deleteCollectorGroupAjax'),
    
    #事件轉開事故
    path('api/incident-rule/edit/', views.editIncidentRuleAjax, name='editIncidentRuleAjax'),
    path('api/incident-rule/load/', views.loadIncidentRuleAjax, name='loadIncidentRuleAjax'),
    
    #數據顯示
    path('api/incident-rule/data/', views.loadPolicyDataAjax, name='loadPolicyDataAjax'),
    
    #事件管理
    path('api/event/list/', views.listEventAjax, name='listEventAjax'),
    
    ]