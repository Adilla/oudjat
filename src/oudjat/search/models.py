from django.db import models
# Create your models here.


class Option(models.Model):
   name = models.CharField(max_length=255)
   description = models.CharField(max_length=255)   
   
   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'options'


class Word(models.Model):
   expression = models.CharField(max_length=255)
   options = models.ManyToManyField(Option, related_name = 'words')

   def __unicode__(self):
       return u'%s' % (self.expression)

   class Meta:
       verbose_name_plural = 'words'
        


class Domain(models.Model):
   name = models.CharField(max_length=255)
   words = models.ManyToManyField(Word, related_name = 'domains')

   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'domains'
 


class Research(models.Model):
   name = models.CharField(max_length=255)
   cron = models.CharField(max_length=255)
   domains = models.ManyToManyField(Domain, related_name = 'researches')

   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'researches'



