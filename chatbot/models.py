from django.db import models

# Create your models here.
class ChatLog(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chatlog({self.user_message})"