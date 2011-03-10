from django.db import models

# Create your models here.
class Conversation(models.Model):
    start_time = models.DateTimeField('time of first question')
    guid = models.CharField(max_length=36)

class Exchange(models.Model):
    conversation = models.ForeignKey(Conversation)
    question_time = models.DateTimeField('when the question was asked')
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=250)

