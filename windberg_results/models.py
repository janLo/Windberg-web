# coding=utf-8
from django.db import models
import windberg_register.models


class ResultTable(models.Model):
    class Meta:
        ordering = ["version", "start_time"]
        permissions = (
            ("import_results", "Can import results from CSV"),
        )

    version = models.ForeignKey(windberg_register.models.Version,
                                verbose_name=u"Laufversion",
                                default=windberg_register.models.Version.current_active_id)
    name = models.CharField(verbose_name=u"Tabellenname", max_length=200)
    slug = models.SlugField(verbose_name=u"Kürzel")
    start_time = models.TimeField(verbose_name=u"Startzeit")
    use_age_group = models.BooleanField(verbose_name=u"Altersklassenwertung", default=True)
    use_gender = models.BooleanField(u"Geschl.-spez. Plätze", default=False)


class ResultEntry(models.Model):
    class Meta:
        ordering = ["table__id", "rank"]

    table = models.ForeignKey(ResultTable, verbose_name=u"Ergebnistabelle", related_name="entries")
    name = models.CharField(verbose_name=u"Name", max_length=200)
    given = models.CharField(verbose_name=u"Vorname", max_length=200)
    start_number =models.IntegerField(verbose_name=u"Startnummer")
    gender = models.CharField(verbose_name=u"Geschlecht", choices=windberg_register.models.Starter.GENDER_CHOICES,
                              max_length=20)
    birth_year = models.DateField(verbose_name=u"GJ", null=True)
    age_group = models.CharField(verbose_name=u"AK", max_length=100)
    club = models.CharField(verbose_name=u"Club", max_length=200)
    rank = models.IntegerField(verbose_name=u"Platz")
    rank_age = models.IntegerField(verbose_name=u"Platz AK")
    rank_sex = models.IntegerField(verbose_name=u"Platz Geschl.")
    result_time = models.TimeField(u"Ergebniszeit")
