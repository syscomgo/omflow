"""omflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from omflow import views
from django.urls.conf import include
from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import static
from django.conf import settings
#from django.contrib import admin
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns  #for active static files


urlpatterns = [
    url(r'^announcement/', include('ommessage.urls')),
    url(r'accounts/', include('omuser.urls')),
    url(r'^flowmanage/', include('omformflow.urls')),
    url(r'^dashboard/', include('omdashboard.urls')),
    url(r'^service/', include('omservice.urls')),
    url(r'^my-mission/', include('ommission.urls')),
    path('',views.home, name='homePage'),
    url(r'^page/file-management/$',views.filePage),
    url(r'^page/403/$',views.noPermissionPage),
    url(r'^rest/(?P<url>.+)$', views.restapi),
    url(r'^page/system/$', views.systemPage),
    url(r'^my-mission/page/myform/(?P<url>.+)$', views.myformpage),
    url(r'^flowmanage/page/myform/(?P<url>.+)$', views.myformpage),
    url(r'^page/sidebar-management/$', views.sidebarManagementPage),
    path('api/system-config/load/', views.loadSystemConfigAjax, name='loadSystemConfigAjax'),
    path('api/system-config/update/', views.updateSystemConfigAjax, name='updateSystemConfigAjax'),
    path('api/files/list/', views.listFilesAjax, name='listFilesAjax'),
    path('api/files/delete/', views.deleteFilesAjax, name='deleteFilesAjax'),
    path('api/disk-status/get/', views.getDiskStatusAjax, name='getDiskStatusAjax'),
    path('api/permission/denied/', views.permissionDenied, name='permissionDenied'),
    path('api/workinfo/load/', views.loadWorkinfoAjax, name='loadWorkinfoAjax'),
    path('api/sidebar-design/load/', views.loadSidebarDesignAjax, name='loadSidebarDesignAjax'),
    path('api/sidebar-design/update/', views.updateSidebarDesignAjax, name='updateSidebarDesignAjax'),
    path('api/sidebar-design/list/', views.listSidebarDesignAjax, name='listSidebarDesignAjax'),
    path('api/l-side/load/', views.loadLSideAjax, name='loadLSideAjax'),
    path('api/ldap-config/check-connect/', views.ldapCheckConnectAjax, name='ldapCheckConnectAjax'),
    path('api/ldap-config/ldap-manual-sync/', views.ldapManualSyncAjax, name='ldapManualSyncAjax'),
    path('api/license-file/upload/', views.uploadLicenseFileAjax, name='uploadLicenseFileAjax'),
    url(r'^api/history-files/download/(?P<path>.+)$', views.downloadHistoryFilesAjax),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    #default
    #path('admin/', admin.site.urls),
]
urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += staticfiles_urlpatterns()   #for active static files