from django.db import models

from datetime import datetime

# Create your models here.
class Conversation(models.Model):
    guid = models.CharField(max_length=36, primary_key=True)
    start_time = models.DateTimeField('time of first question',
            default=datetime.now)

    def num_exchanges(self):
        return self.exchange_set.count()

    def __unicode__(self):
        return unicode(self.start_time)

class Exchange(models.Model):
    conversation = models.ForeignKey(Conversation)
    question_time = models.DateTimeField('when the question was asked',
            default=datetime.now)
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=250)

    def __unicode__(self):
        return self.answer
