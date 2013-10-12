from django.db import models
from cms.models.pluginmodel import CMSPlugin


class SponsorCategory(models.Model):
    name = models.CharField(max_length=100)
    important = models.BooleanField()

    def __unicode__(self):
        return u"Kategorie %s" % self.name

    def is_empty(self):
        return 0 == len(self.active_sponsors().all())

    def active_sponsors(self):
        return self.sponsor_set.filter(active=True)


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(SponsorCategory)
    url = models.URLField()
    image = models.ImageField(upload_to="sponsors/")
    small_image = models.ImageField(upload_to="sponsors/", null=True)
    description = models.TextField(blank=True)
    active = models.BooleanField()

    def __unicode__(self):
        return u"Sponsor %s" % self.name


class CategoryPlugin(CMSPlugin):
    category = models.ForeignKey(SponsorCategory)


