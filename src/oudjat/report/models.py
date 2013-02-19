from django.db import models

# Create your models here.
class Page(models.Model):
    path = models.CharField(max_length=255)
    sitename = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s/%s' % (self.sitename, self.path)
    
    class Meta:
        verbose_name_plural = 'pages'
        db_table = 'report_page'
        unique_together = ("path", "sitename")


class Result(models.Model):
    word = models.ForeignKey('search.Word', related_name='results')
    page = models.ForeignKey(Page, related_name='pages')
    occurences = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s %d' % (self.word, self.page, self.occurences)

    class Meta:
        verbose_name_plural = 'results'
        db_table = 'report_model'
        get_latest_by = 'date'
        order_with_respect_to = 'word'
        order_with_respect_to = 'page'
