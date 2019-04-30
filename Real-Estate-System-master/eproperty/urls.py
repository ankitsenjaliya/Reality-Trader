"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.urls import path, re_path
from eproperty import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('propertylisting/', views.propertylisting, name="propertylisting"),
    # path('propertylisting/<cityName>/', views.propertylisting, name="propertylisting"),
    # path('propertylisting/<cityName>/<provinceName>/', views.propertylisting, name="propertylisting"),
    # path('propertylisting/<cityName>/<provinceName>/<countryName>/', views.propertylisting, name="propertylisting"),

    path('advertisementlisting', views.advertisementlisting, name="advertisementlisting"),
    path('singlePropertyDetails/<int:pk>', views.singlePropertyDetails, name="singlePropertyDetails"),
    path('advertisement', views.advertisement, name="advertisement"),
    path('register', views.register, name="register"),
    path('registartionDetail', views.registartionDetail, name="registartionDetail"),
    path('changePassword', views.changePassword, name="changePassword"),
    path('updateProfile/<int:pk>', views.updateProfile, name="updateProfile"),

    path('useraddProperty/', views.useraddProperty, name='useraddProperty'),
    path('usereditProperty/<int:pk>', views.usereditProperty, name='usereditProperty'),
    path('userdeleteProperty/<int:pk>', views.userdeleteProperty, name='userdeleteProperty'),
    path('manageProperty', views.manageProperty, name="manageProperty"),

# user property image
    path('useraddPropertyImage', views.useraddPropertyImage, name='useraddPropertyImage'),
    path('usereditPropertyImage/<int:pk>', views.usereditPropertyImage, name='usereditPropertyImage'),
    path('userdeletePropertyImage/<int:pk>', views.userdeletePropertyImage, name='userdeletePropertyImage'),
    path('userlistPropertyImage', views.userlistPropertyImage, name='userlistPropertyImage'),


    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('logout/', views.logout, name="logout"),

    # user module
    path('admin_portal/', views.listUser, name='admin_portal'),
    path('admin_portal/addUser/', views.addUser, name='addUser'),
    path('admin_portal/listUserRole/', views.listUserRole, name='listUserRole'),
    path('admin_portal/manageRole/', views.manageRole, name='manageRole'),
    path('admin_portal/editUser/<int:pk>', views.editUser, name='editUser'),
    path('admin_portal/deleteUser/<int:pk>', views.deleteUser, name='deleteUser'),
    path('admin_portal/deleteUserRole/<int:pk>', views.deleteUserRole, name='deleteUserRole'),
    path('admin_portal/listUser/', views.listUser, name='listUser'),
    path('admin_portal/activate_user/', views.activate_user, name='activate_user'),
    path('admin_portal/enable_disable_user/', views.enable_disable_user, name='enable_disable_user'),
    path('admin_portal/listUnapprovedUser/', views.listUnapprovedUser, name='listUnapprovedUser'),

    # role module
    path('admin_portal/addRole/', views.addRole, name='addRole'),
    path('admin_portal/editRole/<int:pk>', views.editRole, name='editRole'),
    path('admin_portal/deleteRole/<int:pk>', views.deleteRole, name='deleteRole'),
    path('admin_portal/listRole/', views.listRole, name='listRole'),

    # features module
    path('admin_portal/addFeature/', views.addFeature, name='addFeature'),
    path('admin_portal/assignFeature/', views.assignFeature, name='assignFeature'),
    path('admin_portal/importFeature/', views.importFeature, name='importFeature'),
    path('admin_portal/editFeature/<int:pk>', views.editFeature, name='editFeature'),
    path('admin_portal/deleteFeature/<int:pk>', views.deleteFeature, name='deleteFeature'),
    path('admin_portal/deleteAssignFeatures/<int:pk>', views.deleteAssignFeatures, name='deleteAssignFeatures'),
    path('admin_portal/listFeature/', views.listFeature, name='listFeature'),
    path('admin_portal/listAssignFeatures/', views.listAssignFeatures, name='listAssignFeatures'),

    # client
    path('view_property', views.view_property, name="view_property"),

    # property
    path('admin_portal/addProperty/', views.addProperty, name='addProperty'),
    path('admin_portal/editProperty/<int:pk>', views.editProperty, name='editProperty'),
    path('admin_portal/deleteProperty/<int:pk>', views.deleteProperty, name='deleteProperty'),
    path('admin_portal/listProperty/', views.listProperty, name='listProperty'),

    # property image
    path('admin_portal/addPropertyImage/', views.addPropertyImage, name='addPropertyImage'),
    path('admin_portal/editPropertyImage/<int:pk>', views.editPropertyImage, name='editPropertyImage'),
    path('admin_portal/deletePropertyImage/<int:pk>', views.deletePropertyImage, name='deletePropertyImage'),
    path('admin_portal/listPropertyImage/', views.listPropertyImage, name='listPropertyImage'),

    # advertisement
    path('admin_portal/addAdvertisement/', views.addAdvertisement, name='addAdvertisement'),
    path('admin_portal/editAdvertisement/<int:pk>', views.editAdvertisement, name='editAdvertisement'),
    path('admin_portal/advertisementConfirmDelete/<int:pk>', views.advertisementConfirmDelete, name='advertisementConfirmDelete'),
    path('admin_portal/listAdvertisement/', views.listAdvertisement, name='listAdvertisement'),

    # user advertisement
    path('useraddAdvertisement', views.useraddAdvertisement, name='useraddAdvertisement'),
    path('usereditAdvertisement/<int:pk>', views.usereditAdvertisement, name='usereditAdvertisement'),
    path('useradvertisementConfirmDelete/<int:pk>', views.useradvertisementConfirmDelete, name='useradvertisementConfirmDelete'),
    path('userlistAdvertisement', views.userlistAdvertisement, name='userlistAdvertisement'),
]
