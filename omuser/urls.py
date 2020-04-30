from django.urls import path
from omuser import views
from django.conf.urls import url

urlpatterns = [
    path('login/',views.loginPage, name='loginPage'),
    path('register/',views.registerPage, name='userRegisterPage'),
    path('logout/', views.logoutPage, name='logout'),
    url(r'^page/password/$', views.changePasswodPage),
    url(r'^page/profile/(?P<url>.+)$', views.profilePage),
    url(r'^page/user-management/$', views.userManagementPage),
    url(r'^page/role-management/$', views.roleManagementPage),
    url(r'^page/group-management/$', views.groupManagementPage),
    url(r'^page/adgroup-management/$', views.adGroupPage),
    url(r'^page/role-detail/(\w*)\/*$', views.roleDetailPage),
    url(r'^page/group-detail/(\w*)\/*$', views.groupDetailPage),
    url(r'^page/adgroup-detail/(\w*)\/*$', views.adGroupDetailPage),
    
    path('api/login/',views.loginAjax, name='loginAjax'),
    path('api/multiple-login/check/',views.checkMultipleLoginAjax, name='checkMultipleLoginAjax'),
    path('api/password/', views.changePasswordAjax, name='changePasswordAjax'),
    path('api/register/',views.registerAjax , name='registerAjax'),
    path('api/user/load/', views.loadUserAjax, name='loadUserAjax'),
    path('api/user/update/', views.updateUserAjax, name='updateUserAjax'),
    path('api/user/list/', views.listUserAjax, name='listUserAjax'),
    path('api/user/add/', views.addUserAjax, name='addUserAjax'),
    path('api/user/delete/', views.deleteUserAjax, name='deleteUserAjax'),
    path('api/user/active/', views.activeUserAjax, name='activeUserAjax'),
    path('api/group/list/', views.listGroupAjax, name='listGroupAjax'),
    path('api/group/add/', views.addGroupAjax, name='addGroupAjax'),
    path('api/group/delete/', views.deleteGroupAjax, name='deleteGroupAjax'),
    path('api/user/group/', views.groupUserAjax, name='groupUserAjax'),
    path('api/group/load/', views.loadGroupAjax, name='loadGroupAjax'),
    path('api/group/update/', views.updateGroupAjax, name='updateGroupAjax'),
    path('api/role/permission/', views.rolePermissionAjax, name='rolePermissionAjax'),
    path('api/users/group/', views.groupUsersAjax, name='groupUsersAjax'),
    path('api/security/get/',views.getSecurityAjax, name='getSecurityAjax'),
    path('api/agree/get/',views.getAgreeAjax, name='getAgreeAjax')
]
