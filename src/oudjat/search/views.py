# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from search.models import Word, Domain, Research, Option
from django import forms
from django.core.validators import validate_email
from django.shortcuts import render, render_to_response
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.template import RequestContext

DOMAINS = [(d.id, d.name) for d in Domain.objects.all()]
OPTIONS = [(o.id, o.name) for o in Option.objects.all()]

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

    return render_to_response('details.html', {'search': w })




def view(request):

    test = Research.objects.all()
    t = loader.get_template('view.html')
    c = Context({
            'test' : test,
            })
    return HttpResponse(t.render(c))



class AddForm(forms.Form):
    word = forms.CharField(max_length=255)
    domain = forms.ChoiceField(widget=RadioSelect(), choices=DOMAINS)
    option = forms.MultipleChoiceField(widget=CheckboxSelectMultiple(), choices=OPTIONS)




def add(request):

   if request.method == 'POST':
       form = AddForm(request.POST)

       if form.is_valid():
           word = form.cleaned_data['word']
           domain = form.cleaned_data['domain']
           option = form.cleaned_data['option']

           w = Word(expression = word)
           w.save()

           for opt in option:
               o = Option.objects.filter(id = opt)
               w.options.add(o.get(pk = opt))

           r = Research(name = word)
           r.save()
            
           d = Domain.objects.filter(id = domain)
           r.domains.add(d.get(pk = domain))
           
           return HttpResponseRedirect('../view/')
   else:
       form = AddForm()

   return render_to_response('add.html', {'form' : form,}, context_instance=RequestContext(request))
        

#def clean_words(self):
#    tmp = Domain.words.count()
   
#    if tmp==100:
#        raise ValidationError("Number of words limit reached")

#    words = self.cleaned_data['words']
#    return words
