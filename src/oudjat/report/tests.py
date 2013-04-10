"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from report.models import *
from search.models import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ModelTest(TestCase):
    
    def setUp(self):
        self.word = Word.objects.create(expression = 'test')
        self.page = Page.objects.create(path = 'test', sitename = 'test')
        self.result = Result.objects.create(word = self.word, page = self.page, occurences = 0)
        

    def test_string(self):
        self.assertEqual(self.page.__unicode__(), 'test/test')
        self.assertEqual(self.result.__unicode__(), 'test test/test 0')
