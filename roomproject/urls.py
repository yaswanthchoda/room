"""roomproject URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from roomapp.views import signup, ProfileView, update_profile, create_room, RoomsView, home, DisplayUsersView, ManageRecords
#, RoomCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('update-profile/', update_profile, name='upd_prf'),
    path('profile/', ProfileView.as_view(), name='prf'),
    path('create_room/', create_room, name='create_room'),
    # path('create_room/', RoomCreateView.as_view(), name='create_room'),
    path('view_room/', RoomsView.as_view(), name='view_room'),
    path('create_user/', signup, name='create_user'),
    # path('display_users/', ProfileView.as_view(), name='display_users'),
    path('display_users/', DisplayUsersView.as_view(), name='display_users'),
    path('get_records/', ManageRecords.as_view(), name='get_records'),
]
