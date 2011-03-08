# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

import therapist

def index(request):
    return render_to_response('index.html',
            context_instance=RequestContext(request))

def ask(request):
    question = request.GET.get('q', None)
    if not question:
        answer = "Ask a question!"
    else:
        answer = therapist.answer(question)

    return render_to_response('question.html', {'answer': answer})

