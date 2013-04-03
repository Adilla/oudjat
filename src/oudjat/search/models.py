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
   options = models.ManyToManyField(Option,
                                    related_name = 'words')

   def __unicode__(self):
       return u'%s' % (self.expression)

   class Meta:
       verbose_name_plural = 'words'
        


class Domain(models.Model):
   name = models.CharField(max_length=255)
   key = models.CharField(max_length=255)

   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'domains'
 

class Crontab(models.Model):
   number_of_researches = models.IntegerField()
   has_reached_limit = models.BooleanField(default = False)

   def __unicode__(self):
      return u'%s' % (self.number_of_researches)


class Research(models.Model):
   name = models.CharField(max_length=255)
   cron = models.ForeignKey(Crontab, related_name= 'crons')
   words = models.CharField(max_length=255)
   domains = models.ManyToManyField(Domain, 
                                    related_name = 'researches')
   is_done = models.BooleanField(default=False)


   def __unicode__(self):
      return u'%s' % (self.name)

   class Meta:
      verbose_name_plural = 'researches'



