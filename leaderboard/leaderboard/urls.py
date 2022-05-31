"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from gui.views import homeView,register_request,login_request,logout_request,profil_view,edit_profile,createTeam_request,teamProfil_view,joinTeam,updateUserRole,removeTeam,updateTeam,removeUser,addUser,createBoard_request,updateBoard,removeBoard,boardProfil_view
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeView),
    path('home/', homeView,name="home"),
    path('register/', register_request,name="register"),
    path("login/", login_request, name="login"),
    path("logout/",logout_request,name="logout"),
    path("profil/",profil_view,name="profil"),
    path("profil/edit/",edit_profile,name="edit"),
    path("createTeam/",createTeam_request,name="createTeam"),
    path("teamProfil/<int:team_id>/",teamProfil_view,name="teamProfil"),
    path("joinTeam/<int:team_id>/",joinTeam,name="joinTeam"),
    path("updateRoleUser/<int:membership_id>/",updateUserRole,name="updateUserRole"),
    path("updateTeam/<int:team_id>/",updateTeam,name="updateTeam"),
    path("removeTeam/<int:team_id>/",removeTeam,name="removeTeam"),
    path("removeUser/<int:membership_id>/",removeUser,name="removeUser"),
    path("addUser/<int:membership_id>/",addUser,name="addUser"),
    path("createBoard/",createBoard_request,name="createBoard"),
    path("updateBoard/<int:board_id>/",updateBoard,name="updateBoard"),
    path("removeBoard/<int:board_id>/",removeBoard,name="removeBoard"),
    path("boardProfil/<int:board_id>/",boardProfil_view,name="boardProfil"),
]
