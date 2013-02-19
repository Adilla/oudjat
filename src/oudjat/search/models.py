from django.db import models
# Create your models here.


class Word(models.Model):
   expression = models.CharField(max_length=255)

   def __unicode__(self):
       return u'%s' % (self.expression)

   class Meta:
       verbose_name_plural = 'words'
       db_table = 'search_word'
       

class Domain(models.Model):
   name = models.CharField(max_length=255)

   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'domains'
      db_table = 'search_domain'

class Research(models.Model):
   name = models.CharField(max_length=255)
   cron = models.CharField(max_length=255)

   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'researches'
      db_table = 'search_research'

class Option(models.Model):
   name = models.CharField(max_length=255)
   description = models.CharField(max_length=255)
   
   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'options'
      db_table = 'search_option'
