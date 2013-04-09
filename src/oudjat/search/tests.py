"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from search.models import *
from report.models import *
from django.utils import timezone
import datetime


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class Add_Launch_Test(TestCase):
    
    def setUp(self):
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
        self.assertEqual(u'%s' % (self.word.expression), 'test')
        self.assertEqual(u'%s' % (self.domain.name), 'test')
        self.assertEqual(u'%s' % (self.research.name), 'test')
       
        self.assertEqual(self.word.expression, 'test') 


    def test_research(self): 

        cmpt = 1
        for obj in Research.objects.all():
            if cmpt == 1:
                self.assertEqual(obj, self.research)
                self.assertNotEqual(obj, self.research2)

            if cmpt == 2:
                self.assertNotEqual(obj, self.research)
                self.assertEqual(obj, self.research2)

            cmpt = cmpt + 1
        
