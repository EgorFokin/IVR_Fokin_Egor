from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.registerUser,name='register'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})',
            views.activate_account,name='activate'),
]