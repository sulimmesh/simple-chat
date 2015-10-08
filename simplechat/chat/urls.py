from django.conf.urls import url
from . import views

urlpatterns =[
	url(r"^$", views.Home.as_view(), name="home"),
	url(r"^login/$", views.Login.as_view(), name="login"),
	url(r"^users/(?P<action>[^/]+)/(?P<username>[^/]+)/$", views.Users.as_view(), name="users"),
]