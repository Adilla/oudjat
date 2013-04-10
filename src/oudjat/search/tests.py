"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from search.models import *
from report.models import *
from search.views import *
from django.utils import timezone
from django.http import *
import datetime



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class LaunchResearchTest(TestCase):
    
    def setUp(self):

        self.option = Option.objects.create(name = 'test', description = 'test')
        self.cron = Crontab.objects.create(number_of_researches = 0, priority = 0)
        self.cron2 = Crontab.objects.create(number_of_researches = 0, priority = 1)
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

    def test_add_cron(self):

        """ Testing that the added crons have the right initial priority """
        
        self.assertEqual(0, self.cron.priority)
        self.assertEqual(1, self.cron2.priority)


    def test_get_cron(self):
        
        """ Testing that the daily cron has the right priority """

        self.assertEqual(0, self.daily.priority)
        self.cron2.priority = (self.cron2.priority - 1) % Crontab.objects.count()
        self.cron2.save()
        self.assertEqual(0, self.cron2.priority)
 

    def test_string(self):
     
        """ Testing returning string """
        self.assertEqual(self.word.__unicode__(), 'test')
        self.assertEqual(self.domain.__unicode__(), 'test')
        self.assertEqual(self.research.__unicode__(), 'test')
        self.assertEqual(self.cron.__unicode__(), u'%s' % (self.cron.id))
        self.assertEqual(self.option.__unicode__(), 'test')
       


    def test_research(self): 

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
    
    def setUp(self):
        self.request = HttpRequest()
        self.request2 = HttpRequest()
        self.request.method = 'POST'
        self.request2.method = 'POST'
       
        self.day = 1
        self.month = 2
        self.year = 2004
        self.pageid = Page.objects.create(sitename = 'test', path = 'test')
        self.domain = Domain.objects.create(name = 'test')
    
        self.choices = forms.ChoiceField(widget=RadioSelect(), 
                                         choices = (self.domain.id, self.domain.name))

        self.request.POST = {'subject' : 'test',
                          'queue' : 'test',
                          'text' : 'test',
                          'requestor' : 'test'}

        self.request2.POST = {'word' : 'test',
                              'domain' : self.domain.id}
   

        self.form = TicketForm(self.request.POST)

   


    def test_index(self):
        self.assertIsInstance(index(self.request), HttpResponse)

    def test_view(self):
        self.assertIsInstance(view(self.request), HttpResponse)

    def test_results(self):
        self.assertIsInstance(results(self.request), HttpResponse)

    def test_report_details(self):
        self.assertIsInstance(report_details(self.request, 
                                             self.year, 
                                             self.month, 
                                             self.day), 
                              HttpResponse)

        
    def test_ticket(self):
        self.assertEqual(self.request.method, 'POST')
        self.assertIsInstance(ticket(self.request, self.year,
                                     self.month, self.day, 
                                     self.pageid.id), 
                              HttpResponse)
        self.assertTrue(self.form.is_valid())
  


    def test_add(self):
        self.assertEqual(self.request2.method, 'POST')
        self.assertIsInstance(add(self.request2), HttpResponse)
  
     
        

