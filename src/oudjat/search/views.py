# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
from search.models import *
from report.models import *
from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.shortcuts import render, render_to_response
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
import datetime, rt


DOMAINS = [(d.id, d.name) for d in Domain.objects.all()]
#OPTIONS = [(o.id, o.name) for o in Option.objects.all()]

def index(request):    
    return render(request, 'index.html',
              {})


def clean(self):
    if any(self.errors):
        return
    data = self.cleaned.data
    return data


def view(request):
    test = Research.objects.all()
    
    return render(request, 'view.html',
              {'test' : test,
               })



def results(request):
    dates = Result.objects.dates('date', 'day', order = 'DESC')
     
    return render(request, 'results.html', {
            'dates' : dates,
            })

def report_details(request, year, month, day):
   
    y = int(year)
    m = int(month)
    d = int(day)
    
    all_pages = Page.objects.filter(
        pages__date = datetime.date(y,m,d)
        ).distinct()
   
    return render_to_response('details.html', 
                             { 'all_pages' : all_pages,
                               'y' : y,
                               'm' : m,
                               'd' : d,
                              },
                             context_instance = RequestContext(request))


class TicketForm(forms.Form):
    subject = forms.CharField(max_length = 255)
    queue = forms.CharField(max_length = 255)
    text = forms.CharField(widget = forms.Textarea)
    requestor = forms.CharField(max_length = 255)


def ticket(request, year, month, day, pageid):
    page = Page.objects.get(pk = int(pageid))

    page_id = int(pageid)
    if request.method == 'POST':
        form = TicketForm(request.POST)
       
        if form.is_valid():
            subject = form.cleaned_data['subject']
            queue = form.cleaned_data['queue']
            text = form.cleaned_data['text']
            requestor = form.cleaned_data['requestor']
  
            login = 'admin'
            passw = 'admin'
 
            tracker = rt.Rt('http://rt.easter-eggs.org/demos/testing/REST/1.0/', login, passw)
        
            if tracker.login() == True:
                num_track = tracker.create_ticket(Queue='Customer Service', 
                                                  Subject = 'test', 
                                                  Text = 'test again and again',
                                                  )
                tracker.edit_ticket(num_track, 
                                    Requestors = 'test')
                
                tracker.logout()


                page.ticket = True
                page.save()
                
            return HttpResponseRedirect('../')
    else:

        form = TicketForm(initial={'subject': page.sitename,
                                   'queue': settings.FILE_RT,
                                   'text': page.path,
                                   'requestor': 'admin@no-mail.com'})

    return render_to_response('ticket.html',
                              {'form' : form,
                               'page_ticket' : page.ticket,
                               'y': year,
                               'm': month,
                               'd': day,
                               'id': pageid},
                              context_instance = RequestContext(request))



class AddForm(forms.Form):
    word = forms.CharField(max_length=255)
    domain = forms.ChoiceField(widget=RadioSelect(), 
                               choices=DOMAINS)
   # option = forms.MultipleChoiceField(widget=CheckboxSelectMultiple(), 
   #                                    choices=OPTIONS)


def add(request):

   if request.method == 'POST':
       form = AddForm(request.POST)

       if form.is_valid():
           word = form.cleaned_data['word']
           domain = form.cleaned_data['domain']
 #         option = form.cleaned_data['option']

           w = Word(expression = word)
           w.save()

           # for opt in option:
           #     o = Option.objects.filter(id = opt)
           #     w.options.add(o.get(pk = opt))

           c = Crontab.objects.filter(has_reached_limit = False)[0]
           
           r = Research(name = word, words = word, cron = c)
           r.save()

           c.number_of_researches = c.number_of_researches + 1

           c.save()
            
           d = Domain.objects.filter(id = domain)
           r.domains.add(d.get(pk = domain))
           
           return HttpResponseRedirect('../view/')
   else:
       form = AddForm()

   return render_to_response('add.html',
                             {'form' : form,}, 
                             context_instance=RequestContext(request)
                             )
        
