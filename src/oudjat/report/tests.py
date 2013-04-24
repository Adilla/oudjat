"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from report.models import Page, Result
from search.models import Word


class ModelTest(TestCase):


    """ Models class test """
    
    def setUp(self):

        """ Defining a word, a page and a result """

        self.word = Word.objects.create(expression = 'test')
        
        self.page = Page.objects.create(
            path = 'test', 
            sitename = 'test')
       
        self.result = Result.objects.create(
            word = self.word, 
            page = self.page, 
            occurences = 0)
        

    def test_string(self):

        """ Testing strings """

        self.assertEqual(self.page.__unicode__(), 'test/test')
        self.assertEqual(self.result.__unicode__(), 'test test/test 0')
