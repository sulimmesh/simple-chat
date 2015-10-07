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
	def get(self, request, username):
		context = {}
		if username == "create":
			template = "new_user.html"
		else:
			template = "user.html"
			profile = models.UserProfile.Get(username)
			context["profile"] = profile
			context["friends"] = profile.friends.all()
			context["chats"] = models.Chat.GetByProfile(profile)
		return render(request, template, context)

	def post(self, request, username):
		context = {}
		username = request.POST["username"]
		password = request.POST["password"]
		new_user = models.UserProfile.Create(username, password)
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			template = "home.html"
		else:
			template = "login.html"
		return render(request, template, context)



