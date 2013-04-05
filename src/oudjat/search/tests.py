"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from search.models import *


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
