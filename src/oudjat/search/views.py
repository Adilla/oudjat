# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader
from search.models import Word, Domain, Research, Option
from django import forms
from django.core.validators import validate_email


def index(request):
    t = loader.get_template('index.html')
    c = Context({           
            })
    return HttpResponse(t.render(c))


def clean(self):
    if any(self.errors):
        return
    data = self.cleaned.data
    return data


def detail(request, search_id):

    return render_to_response('details.html', {'search':w} )

def add(request):
    dom = Domain.objects.all()
    opt = Option.objects.all()
    t = loader.get_template('add.html')
    c = Context({
            'dom' : dom,
            'opt' : opt,
            })
    
    return HttpResponse(t.render(c))


def view(request):

    test = Research.objects.all()
    t = loader.get_template('view.html')
    c = Context({
            'test' : test,
            })
    return HttpResponse(t.render(c))


#def clean_words(self):
#    tmp = Domain.words.count()
   
#    if tmp==100:
#        raise ValidationError("Number of words limit reached")

#    words = self.cleaned_data['words']
#    return words
