from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Topic(models.Model):
    Name            = models.CharField(max_length = 64, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Creator         = models.ForeignKey(User, null = False, blank = False)
    Description     = models.TextField(default= "", null = True, blank = True)

    def __unicode__(self):
        return self.Name

    def admin_url(self):
        return '<a href="/admin/forum/topic/%s/">%s</a>' % (self.id, self.Name)

    class Meta:
        get_latest_by = "Creation_Data"
    

class Post(models.Model):
    Author          = models.ForeignKey(User, null = False, blank = False)
    Topic           = models.ForeignKey(Topic, null = False, blank = False)
    Creation_Data   = models.DateTimeField(default = timezone.now)
    Content         = models.TextField(null = False, blank = False)

    class Meta:
        get_latest_by = "Creation_Data"


    def url(self):
        return '/admin/forum/post/%s/' % self.id