"""
All views
"""

from django.http import HttpResponseRedirect
from django.template import RequestContext
from search.models import Word, Domain, Crontab, Search
from report.models import *
from django import forms
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.forms.widgets import RadioSelect
import datetime, rt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def index(request):    

    """ main page """
    user = request.user.username
    first = request.user.first_name
    last = request.user.last_name
    return render(request, 'index.html',
              {'user' : user,
               'first' : first,
               'last' : last,
               })


def clean(self):
    """ clean method """

    if any(self.errors):
        return
    data = self.cleaned.data
    return data

@login_required
def view(request):

    """ displaying all searches added """
    user = request.user.username
    first = request.user.first_name
    last = request.user.last_name
   
    test = Search.objects.filter(is_done = False)
    
    return render(request, 'view.html',
              {'test' : test,
               'user' : user,
               'first' : first,
               'last' : last,
               })


@login_required
def results(request):
    """ displaying reports per date """
    user = request.user.username
    first = request.user.first_name
    last = request.user.last_name

    dates = Result.objects.dates('date', 'day', order = 'DESC')
     
    return render(request, 'results.html', {
            'dates' : dates,
            'user' : user,
            'first' : first,
            'last' : last,
            })

@login_required
def report_details(request, year, month, day):

    """ displaying details of report """
    user = request.user.username
    first = request.user.first_name
    last = request.user.last_name

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
                               'user' : user,
                               'first' : first,
                               'last' : last,
                              },
                             context_instance = RequestContext(request))


class TicketForm(forms.Form):

    """ Form to send a ticket """

    subject = forms.CharField(max_length = 255)
    queue = forms.CharField(max_length = 255)
    text = forms.CharField(widget = forms.Textarea)
    requestor = forms.CharField(max_length = 255)

@login_required
def ticket(request, year, month, day, pageid):
    """ Handling RT tickets """
    user = request.user.username
    first = request.user.first_name
    last = request.user.last_name

    page = Page.objects.get(pk = int(pageid))

    #page_id = int(pageid)
    if request.method == 'POST':
        form = TicketForm(request.POST)
       
        if form.is_valid():
            subject = form.cleaned_data['subject']
            queue = form.cleaned_data['queue']
            text = form.cleaned_data['text']
            requestor = form.cleaned_data['requestor']
  
            login = user
            passw = request.user.password
 
          #  tracker = rt.Rt(
          #      'http://rt.easter-eggs.org/demos/testing/REST/1.0/', 
          #      login, 
          #      passw)

            tracker = rt.Rt(
                'https://rtdev.unistra.fr/rt/REST/1.0/',
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
                                   'requestor': request.user.email})

    return render_to_response('ticket.html',
                              {'form' : form,
                               'page_ticket' : page.ticket,
                               'y': year,
                               'm': month,
                               'd': day,
                               'id': pageid,
                               'user' : user,
                               'first' : first,
                               'last' : last,
                               },
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
        self.fields['domain'].choices = [
            (d.id, d.name) for d in Domain.objects.all()
            ]

@login_required
def add(request):

    """ Handling the add of a new search """
    user = request.user.username
    first = request.user.first_name
    last = request.user.last_name

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
                    _cron = Crontab(number_of_searches = 0, priority = 0)
                else:
                    _cron = Crontab(number_of_searches = 0, priority = 1)
                    for cron in Crontab.objects.all():
                        if cron.priority != 0:
                            cron.priority = cron.priority + 1
                            cron.save()
               
                _cron.save()
                
            res = Search(name = word, words = word, cron = _cron)
            res.save()

            _cron.number_of_searches = _cron.number_of_searches + 1
          
            if _cron.number_of_searches == 100:
                _cron.has_reached_limit = True
   
            _cron.save()
            
            dom = Domain.objects.filter(id = domain)
            res.domains.add(dom.get(pk = domain))
            
            return HttpResponseRedirect('../view/')
    else:
        form = AddForm()

    return render_to_response('add.html',
                              {'form' : form,
                               'user' : user,
                               'first' : first,
                               'last' : last,}, 
                              context_instance=RequestContext(request)
                              )
        
