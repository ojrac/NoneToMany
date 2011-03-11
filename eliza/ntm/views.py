# Create your views here.
from django.shortcuts import render_to_response

import uuid

from models import Conversation, Exchange
import therapist

def index(request):
    conversation_uuid = uuid.uuid4()
    c = Conversation(guid=conversation_uuid)
    c.save()
    return render_to_response('index.html',
            {'uuid': str(conversation_uuid)})

def ask(request, conversation_uuid):
    question = request.GET.get('q', None)
    if not question:
        answer = "Ask a question!"
    else:
        answer = therapist.answer(question)

        c = Conversation.objects.get(guid=conversation_uuid)
        c.exchange_set.create(question=question, answer=answer)

    return render_to_response('question.html',
            {'answer': answer, 'question': question})

