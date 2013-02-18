from django.db import models
# Create your models here.


class Word(models.Model):
   expression = models.CharField(max_length=255)

   def __unicode__(self):
       return u'%s' % (self.expression)

   class Meta:
       verbose_name_plural = 'words'
       db_table = 'search_word'
       
