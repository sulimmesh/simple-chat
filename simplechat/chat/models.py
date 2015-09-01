from django.db import models

#user class
class User(models.Model):
	username = models.CharField(primary_key=True, max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.username

	@classmethod
	def Get(cls, username):
		users = cls.objects.filter(username=username)
		if users:
			return users[0]
		else:
			return None

	@classmethod
	def Create(cls, username, password):
		users = cls.objects.filter(username=username)
		if len(users) > 0:
			return None
		else:
			user = cls(username=username, password=password)
			user.save()
			return user

	@classmethod
	def Update(cls, username, new_username=None, password=None):
		users = cls.objects.filter(username=username)
		if len(users) == 1:
			user = users[0]
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
		users = cls.objects.filter(username=username)
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
	users = models.ManyToManyField(User)

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
