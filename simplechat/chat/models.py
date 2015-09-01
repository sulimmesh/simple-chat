from django.db import models

#user class
class User(models.Model):
	username = models.CharField(primary_key=True, max_length=100)
	password = models.CharField(max_length=100)

	@classmethod
	def Get(cls, username):
		user = cls.get(username=username)
		if user:
			return user
		else:
			return None

	@classmethod
	def Create(cls, username, password):
		user = cls.get(username=username)
		if user:
			return None
		else:
			user = cls(username=username, password=password)
			user.save()
			return user

	@classmethod
	def Update(cls, username, new_username=None, password=None):
		user = cls.get(username=username)
		if user:
			if new_username:
				user.username = new_username
			if password:
				user.password = password
			user.save()
			return user
		else:
			return None

	@classmethod
	def Delete(cls, username):
		user = cls.get(username=username)
		if user:
			user.delete()
			return True
		else:
			return False

class Message(models.Model):
	text = models.CharField(max_length=500)

	@classmethod
	def Get(cls, text):
		messages = cls.objects.filter(text=text)
		message = messages[0]
		if user:
			return user
		else:
			return None

	@classmethod
	def Create(cls, text):
		message = cls.Get(text)
		if message:
			return None
		else:
			message = cls(text=text)
			message.save()
			return message

	@classmethod
	def Delete(cls, message_id):
		message = cls.get(pk=message_id)
		if message:
			message.delete()
			return True
		else:
			return False

class Chat(models.Model):
	users = models.ManyToManyField(User)
	messages = models.ManyToManyField(Message)

	@classmethod
	def Get(cls, chat_id):
		chat = cls.get(pk=chat_id)
		if chat:
			return chat
		else:
			return None

	@classmethod
	def Create(cls, list_of_users):
		chat = cls()
		for user in list_of_users:
			chat.add(user)
		chat.save()
		return chat

	@classmethod
	def Update(cls, chat_id, list_of_users):
		chat = cls.get(pk=chat_id)
		current_users = chat.users.all()
		if chat:
			for user in list_of_users:
				if not user in list_of_users:
					chat.add(user)
			for user in current_users:
				if not user in list_of_users:
					chat.users.remove(user)
			user.save()
		else:
			return None

	@classmethod
	def Delete(cls, chat_id):
		chat = cls.get(pk=chat_id)
		if chat:
			chat.delete()
			return True
		else:
			return False