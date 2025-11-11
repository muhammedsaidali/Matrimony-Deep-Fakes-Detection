"""
URL configuration for Matrimony project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from MatrimonyApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),  # You can use the root path for index
    path("login/", views.signin, name="login"),
    path("register/", views.register, name="register"),
    path("contact/", views.contact, name="contact"),
    path("commonBase/", views.commonBase, name="common_base"),
    path("userHome/", views.userHome, name="user_home"),
    path("adminHome/", views.adminHome, name="admin_home"),
    path("profile/", views.profile, name="profile"),
    path("uploadProfilePic/", views.uploadProfilePic, name="upload_profile_pic"),
    path("editProfile/", views.editProfile, name="edit_profile"),
    path("approveUser/", views.approveUser, name="approve_user"),
    path("rejectUser/", views.rejectUser, name="reject_user"),
    path("profileDetails/", views.profileDetails, name="profile_details"),
    path("sendInterest/", views.send_interest, name="send_interest"),
    path("approveIntrest/", views.approveIntrest, name="approve_interest"),
    path("rejectIntrest/", views.rejectIntrest, name="reject_interest"),
    path("chat/", views.chat, name="chat"),
    path("chatList/", views.chatList, name="chat_list"),
    path("like/", views.like, name="like"),
    path("dislike/", views.dislike, name="dislike"),
    path("allUsers/", views.allUsers, name="all_users"),
    path("joinmembership/", views.joinmembership, name="join_membership"),
    path("payment/", views.payment, name="payment"),
]


