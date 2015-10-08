from django.conf.urls import url
from . import views

urlpatterns =[
	url(r"^$", views.Home.as_view(), name="home"),
	url(r"^login/$", views.Login.as_view(), name="login"),
	url(r"^users/(?P<action>[^/]+)/(?P<username>[^/]+)/$", views.Users.as_view(), name="users"),
	url(r"^chats/(?P<chat_id>[^/]+)/$", views.Chats.as_view(), name="chats"),
	url(r"^chats/(?P<action>[^/]+)/(?P<id>[^/]+)/$", views.Chats.as_view(), name="chat_actions"),
]