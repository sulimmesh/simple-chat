from django.db import models
from django.contrib.auth.models import User

#user class
class UserProfile(models.Model):
	#this class exists in case more user information would be needed
	#a later date
	user = models.ForeignKey(User, unique=True)
	friends = models.ManyToManyField("self")
	online = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.username)

	@classmethod
	def Get(cls, username):
		all_users = User.objects.all()
		matching_users = all_users.filter(username=username)
		if len(matching_users) > 1 or len(matching_users) < 1:
			return None
		users = cls.objects.filter(user=matching_users[0])
		if users:
			return users[0]
		else:
			return None

	@classmethod
	def GetAll(cls):
		users = cls.objects.all()
		return users

	@classmethod
	def GetOnline(cls):
		users = cls.objects.filter(online=True)
		return users

	@classmethod
	def GetFriends(cls, username):
		user = cls.Get(username)
		return user.friends.all()

	@classmethod
	def AddFriend(cls, username, friend_name):
		user = cls.Get(username)
		friend = cls.Get(friend_name)
		user.friends.add(friend)
		return user.friends.all()

	@classmethod
	def removeFriend(cls, username, friend_name):
		user = cls.Get(username)
		friend = cls.Get(friend_name)
		user.friends.remove(friend)
		return user.friends.all()	

	@classmethod
	def Create(cls, username, password):
		all_users = User.objects.all()
		matching_users = all_users.filter(username=username)
		if len(matching_users) > 0:
			return None
		else:
			login_user = User.objects.create_user(username=username, 
				password=password)
			login_user.save()
			new_user = cls(user=login_user, online=True)
			new_user.save()
			return new_user

	@classmethod
	def Update(cls, username, new_username=None, password=None, online=None):
		all_users = User.objects.all()
		matching_users = all_users.filter(username=username)
		if len(matching_users) > 1 or len(matching_users) < 1:
			return None
		users = cls.objects.filter(user=matching_users[0])
		if len(users) == 1:
			user = users[0]
			if new_username:
				user.users.all()[0].username = new_username
			if password:
				user.users.all()[0].password = password
			user.user.save()
			if online:
				user.online = True
			user.save()
			return user
		else:
			return None


	@classmethod
	def Delete(cls, username):
		all_users = User.objects.all()
		matching_users = all_users.filter(username=username)
		if len(matching_users) > 1 or len(matching_users) < 1:
			return None
		users = cls.objects.filter(user=matching_users[0])
		if len(users) == 1:
			user = users[0]
			user.delete()
			return True
		else:
			return False

class Message(models.Model):
	text = models.CharField(max_length=500)
	chat = models.ForeignKey("Chat")

	def __str__(self):
		return str(chat)+": "+self.text

	@classmethod
	def Get(cls, message_id):
		messages = cls.objects.filter(id=message_id)
		message = messages[0]
		if message:
			return message
		else:
			return None

	@classmethod
	def GetByChat(cls, chat):
		messages = cls.objects.filter(chat=chat)
		if len(messages) < 1:
			return None
		else:
			return messages

	@classmethod
	def Create(cls, text, chat):
		message = cls(text=text, chat=chat)
		message.save()
		return message

	@classmethod
	def Delete(cls, message_id):
		messages = cls.objects.filter(id=message_id)
		if len(messages) < 1:
			return False
		message = messages[0]
		message.delete()
		return True

class Chat(models.Model):
	users = models.ManyToManyField(UserProfile)

	def __str__(self):
		return str(self.id)

	@classmethod
	def Get(cls, chat_id):
		chats = cls.objects.filter(pk=chat_id)
		if len(chats) < 1:
			return None
		chat = chats[0]
		if chat:
			return chat
		else:
			return None

	@classmethod
	def GetByProfile(cls, profile):
		chats = cls.objects.filter(users=profile)
		return chats

	@classmethod
	def Create(cls, list_of_users):
		chat = cls()
		chat.save()
		for user in list_of_users:
			chat.users.add(user)
		chat.save()
		return chat

	@classmethod
	def Update(cls, chat_id, list_of_users):
		chats = cls.objects.filter(pk=chat_id)
		if len(chats) < 1:
			return None
		chat = chats[0]
		current_users = chat.users.all()
		for user in list_of_users:
			if not user in list_of_users:
				chat.users.add(user)
		for user in current_users:
			if not user in list_of_users:
				chat.users.remove(user)
		user.save()

	@classmethod
	def Delete(cls, chat_id):
		chats = cls.objects.filter(pk=chat_id)
		if len(chats) < 1:
			return False
		chat = chats[0]
		chat.delete()
		return True
