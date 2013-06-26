"""
Models related to search
"""

from django.db import models
# Create your models here.

class Option(models.Model):
    """ Defining an option """

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)   
   
    def __unicode__(self):
       return u'%s' % (self.name)
    
    class Meta:
       verbose_name_plural = 'options'
       

class Word(models.Model):
   

    """ Defining a word """

    expression = models.CharField(max_length=255)
    options = models.ManyToManyField(Option,
                                     related_name = 'words')

    def __unicode__(self):
       return u'%s' % (self.expression)
    
    class Meta:
       verbose_name_plural = 'words'
       


class Domain(models.Model):

    """ Defining a domain """

    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)

    def __unicode__(self):
       return u'%s' % (self.name)

    class Meta:
       verbose_name_plural = 'domains'
 

class Crontab(models.Model):

    """ Defining a cron """ 

    number_of_searches = models.IntegerField()
    has_reached_limit = models.BooleanField(default = False)
    priority = models.IntegerField()
    
    def __unicode__(self):
       
       return u'%s' % (self.id)


class Search(models.Model):

    """ Defining a search """

    name = models.CharField(max_length=255)
    cron = models.ForeignKey(Crontab, related_name= 'crons')
    words = models.CharField(max_length=255)
    domains = models.ManyToManyField(Domain, 
                                     related_name = 'searches')
    is_done = models.BooleanField(default=False)


    def __unicode__(self):
       return u'%s' % (self.name)

    class Meta:
       verbose_name_plural = 'searches'



