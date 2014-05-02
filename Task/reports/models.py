from django.db import models
import datetime
from django.utils import timezone

class Reports(models.Model):
    title = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.title
    def was_published_recently(self):
    	now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Text(models.Model):
    reports = models.ForeignKey(Reports)
    reports_text = models.CharField(max_length=350)
    browsed = models.IntegerField(default=0)
    def __unicode__(self):
        return self.reports_text
