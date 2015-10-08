from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from . import models

# Create your views here.
class Home(View):
	def get(self, request):
		context = {}
		if request.user.is_authenticated():
			user = request.user
			profile = models.UserProfile.Get(user.username)
			context["profile"] = profile
			template = "home.html"
		else:
			template = "login.html"
		return render(request, template, context)

	def post(self, request):
		pass


class Login(View):
	def get(self, request):
		context = {}
		template = "login.html"
		return render(request, template, context)

	def post(self, request):
		context = {}
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			template = "home.html"
		else:
			template = "login.html"
		return render(request, template, context)

class Users(View):
	def get(self, request, action, username):
		context = {}
		if action == "create":
			template = "new_user.html"
		elif action == "view":
			if username == "all":
				template = "users.html"
				profile = models.UserProfile.Get(username)
				context["profile"] = profile
				profiles = models.UserProfile.GetAll()
				context["profiles"] = profiles
			else:
				template = "user.html"
				profile = models.UserProfile.Get(username)
				context["profile"] = profile
				context["friends"] = profile.friends.all()
				context["chats"] = models.Chat.GetByProfile(profile)
		return render(request, template, context)

	def post(self, request, action, username):
		context = {}
		if action == "create":
			username = request.POST["username"]
			password = request.POST["password"]
			new_user = models.UserProfile.Create(username, password)
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				template = "home.html"
			else:
				template = "login.html"
		elif action == "add":
			friend = models.UserProfile.Get(username)
			user = request.user
			profile = models.UserProfile.Get(user.username)
			friends_list = models.UserProfile.AddFriend(profile.user.username, 
				friend.user.username)
			context["profile"] = profile
			context["profiles"] = models.UserProfile.GetAll()
			template = "users.html"
		return render(request, template, context)



