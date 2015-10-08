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

class Chats(View):
	def get(self, request, *args, **kwargs):
		context = {}
		chat_id = kwargs["chat_id"]
		context["chat"] = models.Chat.Get(chat_id)
		context["messages"] = models.Message.GetByChat(models.Chat.Get(chat_id))
		context["profiles"] = models.Chat.GetProfiles(chat_id)
		template = "chat.html"
		return render(request, template, context)

	def post(self, request, *args, **kwargs):
		context = {}
		action = None
		username = None
		chat_id = None
		if "action" in kwargs.keys():
			action = kwargs["action"]
		if action == "invite":
			username = kwargs["id"]
			friends = models.UserProfile.GetFriends(request.user.username)
			friend = models.UserProfile.Get(username)
			profile = models.UserProfile.Get(request.user.username)
			new_chat = models.Chat.Create([profile, friend])
			context["friends"] = friends
			context["profile"] = profile
			context["chats"] = models.Chat.GetByProfile(profile)
			template = "user.html"
		elif action == "message":
			chat_id = kwargs["id"]
			text = request.POST["text"]
			chat = models.Chat.Get(chat_id)
			profile = models.UserProfile.Get(request.user.username)
			message = models.Message.Create(text, profile, chat)
			context["chat"] = models.Chat.Get(chat_id)
			context["messages"] = models.Message.GetByChat(chat)
			context["profile"] = profile
			template = "chat.html"
		return render(request, template, context)



