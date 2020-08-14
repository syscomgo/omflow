from django.urls import path
from omformflow import views
from django.conf.urls import url

urlpatterns = [
    url(r'^page/flow-app/$', views.flowAppManagePage),
    url(r'^page/flowManagePage/(?P<url>.+)$', views.flowManagePage),
    url(r'^page/workflow-app/$', views.workflowAppManagePage),
    url(r'^page/workflowManagePage/(?P<url>.+)$', views.workflowManagePage),
    url(r'^page/scheduleflowManagePage/$', views.scheduleflowManagePage),
    url(r'^page/flowCreatePage/$', views.flowCreatePage),
    url(r'^page/flowDesignPage/(?P<url>.+)$', views.flowDesignPage),
    url(r'^page/workflowPage/(?P<url>.+)$', views.workflowPage),
    url(r'^page/flowvaluePage/(?P<url>.+)$', views.flowvaluePage),
    url(r'^page/parameterPage/$', views.parameterPage),
    url(r'^page/SLAManagePage/$', views.SLAManagePage),
    #應用設計-app
    path('api/flow-workspace-app/edit/', views.editWorkspaceApplicationAjax, name='editWorkspaceApplicationAjax'),
    path('api/flow-workspace-app/list/', views.listWorkspaceApplicationAjax, name='listWorkspaceApplicationAjax'),
    path('api/flow-workspace-app/deploy/', views.deployWorkspaceApplicationAjax, name='deployWorkspaceApplicationAjax'),
    path('api/flow-workspace-app/export/', views.exportWorkspaceApplicationAjax, name='exportWorkspaceApplicationAjax'),
    path('api/flow-workspace-app/import/', views.importWorkspaceApplicationAjax, name='importWorkspaceApplicationAjax'),
    path('api/flow-workspace-app-language/export/', views.exportAppLanguagePackageAjax, name='exportAppLanguagePackageAjax'),
    path('api/flow-workspace-app-language/import/', views.importAppLanguagePackageAjax, name='importAppLanguagePackageAjax'),
    #應用設計-流程
    path('api/flow-workspace/create/', views.createFlowWorkspaceAjax, name='createFlowWorkspaceAjax'),
    path('api/flow-workspace/list/', views.listFlowWorkspaceAjax, name='listFlowWorkspaceAjax'),
    path('api/flow-workspace/update/', views.updateFlowWorkspaceAjax, name='updateFlowWorkspaceAjax'),
    path('api/flow-workspace/load/', views.loadFlowWorkspaceAjax, name='loadFlowWorkspaceAjax'),
    path('api/flow-workspace/delete/', views.deleteFlowWorkspaceAjax, name='deleteFlowWorkspaceAjax'),
    path('api/flow-workspace/copy/', views.copyFlowWorkspaceAjax, name='copyFlowWorkspaceAjax'),
    path('api/flow-workspace-outside/get/', views.getOutsideFlowAjax, name='getOutsideFlowAjax'),
    path('api/flow-workspace-inside/get/', views.getInsideFlowAjax, name='getInsideFlowAjax'),
#     path('api/flow-version/list/', views.listFlowVersionAjax, name='listFlowVersionAjax'),
    #已上架應用-流程
    path('api/flow-active/list/', views.listFlowActiveAjax, name='listFlowActiveAjax'),
    path('api/flow-active/update/', views.updateFlowActiveAjax, name='updateFlowActiveAjax'),
    path('api/flow-active/active/', views.activeFlowActiveAjax, name='activeFlowActiveAjax'),
    #已上架應用-app
    path('api/flow-active-app/export/', views.exportActiveApplicationAjax, name='exportActiveApplicationAjax'),
    path('api/flow-active-app/undeploy/', views.undeployActiveApplicationAjax, name='undeployActiveApplicationAjax'),
    path('api/flow-active-app/redeploy/', views.redeployActiveApplicationAjax, name='redeployActiveApplicationAjax'),
    path('api/flow-active-app/list/', views.listActiveApplicationAjax, name='listActiveApplicationAjax'),
    #自訂應用-取得表頭
    path('api/flow-active-display-field/get/', views.getFlowActiveDisplayFieldAjax, name='getFlowActiveDisplayFieldAjax'),
    #自訂應用-取得流程api格式
    path('api/flow-active-api-format/get/', views.getFlowAPIFormatAjax, name='getFlowAPIFormatAjax'),
    path('api/omdata-data-id/get/<str:api_path>/', views.getDataIDListAjax, name='getDataIDListAjax'),
#     url('api/omdata-data-id/get/([a-z0-9-]+)', views.getDataIDListAjax, name='getDataIDListAjax'),
    #排程設定
    path('api/flow-active/schedule/', views.scheduleFlowActiveAjax, name='scheduleFlowActiveAjax'),
    path('api/flow-active/schedule/list/', views.listSchedulerAjax, name='listSchedulerAjax'),
    path('api/schedule/active/', views.activeScheduleAjax, name='activeScheduleAjax'),
    
    path('api/form-design/load/', views.loadFormDesignAjax, name='loadFormDesignAjax'),
    path('api/flow-display/get/', views.getFlowFieldNameAjax, name='getFlowFieldNameAjax'),
    path('api/flow-name/load/', views.getApplicationFlowNameAjax, name='getApplicationFlowNameAjax'),
    path('api/omdata/edit/<str:api_path>/', views.editOmDataAjax, name='editOmDataAjax'),
#     url('api/omdata/edit/([a-z0-9-]*)', views.editOmDataAjax, name='editOmDataAjax'),
    path('api/omdata/list/<str:api_path>/', views.listOmDataAjax, name='listOmDataAjax'),
#     url('api/omdata/list/([a-z0-9-]*)', views.listOmDataAjax, name='listOmDataAjax'),
    path('api/omdata/load/', views.loadOmDataAjax, name='loadOmDataAjax'),
    path('api/omdata-file/upload/', views.uploadOmdataFilesAjax, name='uploadOmdataFilesAjax'),
    path('api/omdata-file/list/', views.listOmDataFilesAjax, name='listOmDataFilesAjax'),
    path('api/omdata-history/list/', views.listOmDataHistoryAjax, name='listOmDataHistoryAjax'),
    path('api/omdata-worklog/create/', views.createOmDataWorkLogAjax, name='createOmDataWorkLogAjax'),
    path('api/omdata-worklog/list/', views.listOmDataWorkLogAjax, name='listOmDataWorkLogAjax'),
    path('api/flow-value/get/', views.getFlowValueAjax, name='getFlowValueAjax'),
    path('api/flow-value/update/', views.updateFlowValueAjax, name='updateFlowValueAjax'),
    path('api/flow-object/load/', views.loadFlowObjectAjax, name='loadFlowObjectAjax'),
    path('api/cloud-flow/get/', views.getCloudFlowAjax, name='getCloudFlowAjax'),
    #關聯操作
    path('api/relation/list/', views.listOmDataRelationAjax, name='listOmDataRelationAjax'),
    path('api/relation/edit/', views.editOmDataRelationAjax, name='editOmDataRelationAjax'),
    path('api/relation/data/', views.listOmData4RelationAjax, name='listOmData4RelationAjax'),
    path('api/relation/active/list/', views.listActiveApplication4RelationAjax, name='listActiveApplication4RelationAjax'),
    #日誌操作
    path('api/omdata-worklog/create/', views.createOmDataWorkLogAjax, name='createOmDataWorkLogAjax'),
    path('api/omdata-worklog/list/', views.listOmDataWorkLogAjax, name='listOmDataWorkLogAjax'),
    #參數管理
    path('api/omparameter/list/', views.listOmParameterAjax, name='listOmParameterAjax'),
    path('api/omparameter/create/', views.createOmParameterAjax, name='createOmParameterAjax'),
    path('api/omparameter/update/', views.updateOmParameterAjax, name='updateOmParameterAjax'),
    path('api/omparameter/delete/', views.deleteOmParameterAjax, name='deleteOmParameterAjax'),
    path('api/omparameter/export/', views.exportOmParameterAjax, name='exportOmParameterAjax'),
    path('api/omparameter/import/', views.importOmParameterAjax, name='importOmParameterAjax'),
    #node
    path('api/node-policy/receive/', views.receivePolicyAjax, name='receivePolicyAjax'),
    #SLA
    path('api/flow-SLA/list/', views.listSLARuleAjax, name='listSLARuleAjax'),
    path('api/flow-SLA/create/', views.createSLARuleAjax, name='createSLARuleAjax'),
    path('api/flow-SLA/update/', views.updateSLARuleAjax, name='updateSLARuleAjax'),
    path('api/flow-SLA/delete/', views.deleteSLARuleAjax, name='deleteSLARuleAjax'),
    path('api/flow-SLA-data/list/', views.listSLADataAjax, name='listSLADataAjax'),
    
    #子查詢
    path('api/omdata-sub-query/list/', views.listOmDataForSubQueryAjax, name='listOmDataForSubQueryAjax'),
    path('api/omdata-sub-query/load/', views.loadOmDataForSubQueryAjax, name='loadOmDataForSubQueryAjax'),
    path('api/flow-display-sub-query/get/', views.getFlowFieldNameForSubQueryAjax, name='getFlowFieldNameForSubQueryAjax'),
    
    ]