"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from search.models import Crontab, Word, Research, Option, Domain
from report.models import Page, Result
from search.views import *
from django.utils import timezone
from django import forms
from django.http import HttpResponse, HttpRequest
import datetime
import unittest


class LaunchResearchTest(TestCase):

    """ Class test for launch_research.py """
    
    def setUp(self):

        """
        """

        self.option = Option.objects.create(
            name = 'test',
            description = 'test')

        self.cron = Crontab.objects.create(
            number_of_researches = 0, 
            priority = 0)

        self.cron2 = Crontab.objects.create(
            number_of_researches = 0, 
            priority = 1)

        self.daily = Crontab.objects.get(priority = 0)
     
        self.word = Word.objects.create(expression = 'test')
        self.word2 = Word.objects.create(expression = 'test2')

        self.domain = Domain.objects.create(name = 'test', key = 'test')
     
        self.research = Research.objects.create(name = 'test', 
                                                cron = self.cron,
                                                words = 'test')
      
        self.research2 = Research.objects.create(name = 'test2', 
                                                 cron = self.cron2,
                                                 words = 'test2')

        self.page = Page.objects.create(sitename = 'test', path = 'test')
        self.page2 = Page.objects.create(sitename = 'test2', path = 'test2')

        self.result = Result.objects.create(page = self.page, 
                                            word = self.word, 
                                            date = timezone.now(),
                                            occurences = 0)


        self.result2 = Result.objects.create(page = self.page2,
                                             word = self.word2,
                                             date = timezone.now(),
                                             occurences = 0)

        self.tmp_date = Result.objects.dates('date', 'day', order = 'DESC')


        self.total = Crontab.objects.count()

    def test_add_cron_right(self):

        """ Testing that the added crons have the right initial priority """
        
        if self.total == 0:
            self.assertEqual(0, self.cron.priority)
        else:
            self.assertEqual(1, self.cron2.priority)


    @unittest.expectedFailure
    def test_add_cron_wrong(self):

        """ 
        Testing that error is raised 
        when the wrong priority is given to added crons 
        """


        self.assertNotEqual(0, self.cron.priority, 
                            "Wrong priority : must be equal to 0")
        
        self.assertNotEqual(1, self.cron2.priority, 
                            "Wrong priority : must be equal to 1")
 
    def test_get_cron_right(self):
        
        """ Testing that the daily cron has the right priority """

        self.assertEqual(0, self.daily.priority)
        self.cron2.priority = (self.cron2.priority - 1) % Crontab.objects.count()
        self.cron2.save()
        self.assertEqual(0, self.cron2.priority)


    @unittest.expectedFailure
    def test_get_cron_wrong(self):
        
        """ 
        Testing that the daily cron with a wrong priority raises an error 
        """

        self.assertNotEqual(0, self.daily.priority)
        self.cron2.priority = (self.cron2.priority - 1) % Crontab.objects.count()
        self.cron2.save()
        self.assertNotEqual(0, self.cron2.priority)       
 

    def test_string_right(self):
     
        """ Testing returning string """
        self.assertEqual(self.word.__unicode__(), 'test')
        self.assertEqual(self.domain.__unicode__(), 'test')
        self.assertEqual(self.research.__unicode__(), 'test')
        self.assertEqual(self.cron.__unicode__(), u'%s' % (self.cron.id))
        self.assertEqual(self.option.__unicode__(), 'test')

    @unittest.expectedFailure
    def test_string_wrong(self):

        """ Testing that error is raised when wrong string is given """
        self.assertNotEqual(self.word.__unicode__(), 'test')
        self.assertNotEqual(self.domain.__unicode__(), 'test')
        self.assertNotEqual(self.research.__unicode__(), 'test')
        self.assertNotEqual(self.cron.__unicode__(), u'%s' % (self.cron.id))
        self.assertNotEqual(self.option.__unicode__(), 'test')




    def test_research(self): 

        """ Testing that boolean value of a research is correct """

        cmpt = 1
        for obj in Research.objects.all():
            self.assertFalse(obj.is_done)

            if cmpt == 1:
                self.assertEqual(obj, self.research)
                self.assertNotEqual(obj, self.research2)

            if cmpt == 2:
                self.assertNotEqual(obj, self.research)
                self.assertEqual(obj, self.research2)

            cmpt = cmpt + 1


        
class ViewTest(TestCase):

    """ Class test for views """
    
    def setUp(self):
        """
        """

        self.request = HttpRequest()
        self.request2 = HttpRequest()
        self.request.method = 'POST'
        self.request2.method = 'POST'
       
        self.day = 1
        self.month = 2
        self.year = 2004
        self.pageid = Page.objects.create(sitename = 'test', path = 'test')
        self.domain2 = Domain.objects.create(name = 'test')
    
        self.choices = forms.ChoiceField(
            widget=RadioSelect(), 
            choices = (self.domain2.id, 
                       self.domain2.name)
            )

        self.request.POST = {'subject' : 'test',
                          'queue' : 'test',
                          'text' : 'test',
                          'requestor' : 'test'}

        self.request2.POST = {'word' : 'test',
                              'domain' : str(self.domain2.id)}
   

        self.form = TicketForm(self.request.POST)
        self.form2 = AddForm(self.request2.POST)
        self.form2_bis = AddForm()


    def test_index(self):

        """ Testing that the index view gives a HttpResponse """
        self.assertIsInstance(index(self.request), HttpResponse)

    def test_view(self):

        """ Testing that the view of searches gives a HttpResponse """
        self.assertIsInstance(view(self.request), HttpResponse)

    def test_results(self):

        """ Testing that the view of results gives a HttpResponse """
        self.assertIsInstance(results(self.request), HttpResponse)

    def test_report_details(self):
        """ Testing that the view of details gives a HttpResponse """

        self.assertIsInstance(report_details(self.request, 
                                             self.year, 
                                             self.month, 
                                             self.day), 
                              HttpResponse)

        
    def test_ticket_right(self):

        """ Testing that a ticket form has the right method, 
        http answer, and that the form is valid
        """
       
        self.assertEqual(self.request.method, 'POST')
        self.assertIsInstance(ticket(self.request, self.year,
                                     self.month, self.day, 
                                     self.pageid.id), 
                              HttpResponse)
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean(), self.form.cleaned_data)
 
    @unittest.expectedFailure
    def test_ticket_wrong(self):
        """ 
        Testing that the form ticket is 
        effectively wrong when method not equal POST 
        """
    
        self.assertNotEqual(self.request.method, 'POST')

    def test_add(self):
        """
        Testing that the add form has the right method, http answer,
        and that the form is valid 
        
        """

        self.assertEqual(self.request2.method, 'POST')
        self.assertIsInstance(add(self.request2), HttpResponse)
 
        self.assertTrue(self.form2.is_valid())
        self.assertEqual(self.form2.clean(), self.form2.cleaned_data)

        self.request2.method = ''
        if self.assertEqual(self.request2.method, ''):
            self.assertIsInstance(self.form2_bis, Form)

   
