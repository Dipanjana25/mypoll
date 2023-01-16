from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question = models.CharField(max_length=200)
    created_by = models.ForeignKey(User ,on_delete=models.CASCADE, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    # vote = models.IntegerField(default=0)

    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['created_on']

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()
    votes = models.IntegerField(default=0)

class Notification(models.Model):
    has_voted = [models.IntegerField(default=0)]
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    noti = []