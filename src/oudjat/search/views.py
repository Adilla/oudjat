"""

All views

"""

from django.http import HttpResponseRedirect
from django.template import RequestContext
from search.models import Word, Domain, Crontab, Research
from report.models import *
from django import forms
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.forms.widgets import RadioSelect
import datetime, rt


#DOMAINS = [(d.id, d.name) for d in Domain.objects.all()]
#OPTIONS = [(o.id, o.name) for o in Option.objects.all()]


def index(request):    

    """ main page """
    
    return render(request, 'index.html',
              {})


def clean(self):
    """ clean method """

    if any(self.errors):
        return
    data = self.cleaned.data
    return data


def view(request):

    """ displaying all searches added """

    test = Research.objects.all()
    
    return render(request, 'view.html',
              {'test' : test,
               })



def results(request):
    """ displaying reports per date """

    dates = Result.objects.dates('date', 'day', order = 'DESC')
     
    return render(request, 'results.html', {
            'dates' : dates,
            })

def report_details(request, year, month, day):

    """ displaying details of report """
   
    _year = int(year)
    _month = int(month)
    _day = int(day)
    
    all_pages = Page.objects.filter(
        pages__date = datetime.date(_year, _month, _day)
        ).distinct()
   
    return render_to_response('details.html', 
                             { 'all_pages' : all_pages,
                               'y' : _year,
                               'm' : _month,
                               'd' : _day,
                              },
                             context_instance = RequestContext(request))


class TicketForm(forms.Form):

    """ Form to send a ticket """

    subject = forms.CharField(max_length = 255)
    queue = forms.CharField(max_length = 255)
    text = forms.CharField(widget = forms.Textarea)
    requestor = forms.CharField(max_length = 255)


def ticket(request, year, month, day, pageid):
    """ Handling RT tickets """

    page = Page.objects.get(pk = int(pageid))

    #page_id = int(pageid)
    if request.method == 'POST':
        form = TicketForm(request.POST)
       
        if form.is_valid():
            subject = form.cleaned_data['subject']
            queue = form.cleaned_data['queue']
            text = form.cleaned_data['text']
            requestor = form.cleaned_data['requestor']
  
            login = 'admin'
            passw = 'admin'
 
            tracker = rt.Rt(
                'http://rt.easter-eggs.org/demos/testing/REST/1.0/', 
                login, 
                passw)
        
            if tracker.login() == True:
                num_track = tracker.create_ticket(Queue = queue, 
                                                  Subject = subject, 
                                                  Text = text,
                                                  )
                tracker.edit_ticket(num_track, 
                                    Requestors = requestor)
                
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
    """ Form to add a new search """

    word = forms.CharField(max_length=255)
    domain = forms.ChoiceField(widget=RadioSelect(), 
                               choices=[])
   # option = forms.MultipleChoiceField(widget=CheckboxSelectMultiple(), 
   #                                    choices=OPTIONS)

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.fields['domain'].choices = [(d.id, d.name) for d in Domain.objects.all()]


def add(request):

    """ Handling the add of a new search """

    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            word = form.cleaned_data['word']
            domain = form.cleaned_data['domain']
#         option = form.cleaned_data['option']

            Word.objects.get_or_create(expression = word)

           # for opt in option:
           #     o = Option.objects.filter(id = opt)
           #     w.options.add(o.get(pk = opt))


            try :
                _cron = Crontab.objects.filter(has_reached_limit = False)[0]
           
            except IndexError:
                num = Crontab.objects.count()
               
                if num == 0:
                    _cron = Crontab(number_of_researches = 0, priority = 0)
                else:
                    _cron = Crontab(number_of_researches = 0, priority = 1)
                    for cron in Crontab.objects.all():
                        if cron.priority != 0:
                            cron.priority = cron.priority + 1
                            cron.save()
               
                _cron.save()

            res = Research(name = word, words = word, cron = _cron)
            res.save()

            _cron.number_of_researches = _cron.number_of_researches + 1
          
            if _cron.number_of_researches == 100:
                _cron.has_reached_limit = True
   
            _cron.save()
            
            dom = Domain.objects.filter(id = domain)
            res.domains.add(dom.get(pk = domain))
           
            return HttpResponseRedirect('../view/')
    else:
        form = AddForm()

    return render_to_response('add.html',
                              {'form' : form,}, 
                              context_instance=RequestContext(request)
                              )
        
