# vim: set encoding=utf8
import datetime
from dateutil.relativedelta import relativedelta

from django.db import models


class AgeGroup(models.Model):
    GENDER_CHOICES = (
        ("M", u"männlich"),
        ("F", u"weiblich")
    )

    name = models.CharField(max_length=80)
    short = models.CharField(max_length=40)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    is_pseudo = models.BooleanField()
    is_detail = models.BooleanField()

    def __unicode__(self):
        return u"Ak %s: %d - %d" % (self.name, self.min_age, self.max_age)


    @staticmethod
    def select_from_birth_qry(birth, gender, for_date=None):
        if for_date is None:
            for_date = datetime.datetime.now()
        age = for_date.year - birth.year
        return AgeGroup.objects.filter(
            is_detail=False
        ).filter(
            gender=gender
        ).filter(
            max_age__gte=age
        ).filter(
            min_age__lte=age
        )

    @staticmethod
    def select_from_birth(birth, gender, for_date=None):
        """Create a agegroup(s) instance or a given birth date

        :type birth: datetime.date
        :param birth: The birth date of the Person
        :type gender: basestring
        :param gender: The gender of the Person.
        :type for_date: datetime.datetime
        :param for_date: The datetime the the age should calculated for (now if None)
        :rtype: list of AgeGroup
        """
        return AgeGroup.select_from_birth_qry(birth, gender, for_date).all()


class Run(models.Model):
    name = models.CharField(max_length=100, blank=True)
    distance = models.IntegerField()
    has_ages = models.BooleanField()
    possible_ages = models.ManyToManyField(AgeGroup)

    def real_possible_ages(self):
        ages = set()
        for group in self.possible_ages.all():
            ages.update(range(group.min_age, group.max_age + 1))
        return sorted(list(ages))

    def year_spec(self):
        sorted_ages = self.real_possible_ages()
        groups = []
        cur_group = (sorted_ages[0], sorted_ages[0])
        for age in sorted_ages[1:]:
            if (age - 1) == cur_group[1]:
                cur_group = (cur_group[0], age)
            else:
                groups.append(cur_group)
                cur_group = (age, age)
        groups.append(cur_group)

        active_version = Version.current_active()
        if active_version is None:
            active_date = datetime.datetime.now()
        else:
            active_date = active_version.date
        formatted = []
        for group in groups:
            min_year = active_date - relativedelta(years=group[0])
            max_year = active_date - relativedelta(years=group[1])

            if group[1] > 100:
                formatted.append("ab %s" % min_year.strftime("%y"))
            elif group[1] == group[0]:
                formatted.append("%s" % min_year.strftime("%y"))
            elif (group[1] - group[0]) == 1:
                formatted.append("%s / %s" % (min_year.strftime("%y"), max_year.strftime("%y")))
            else:
                formatted.append("%s - %s" % (min_year.strftime("%y"), max_year.strftime("%y")))
        return formatted

    class Meta:
        ordering = ["distance"]

    def __unicode__(self):
        return u"Run(%dm %s)" % (self.distance, self.name)


class Start(models.Model):
    class Meta:
        ordering = ["start_time", "-creation_date"]

    creation_date = models.DateField(auto_now=True)
    start_time = models.TimeField()
    runs = models.ManyToManyField(Run)


    def __unicode__(self):
        return u"%s angelegt: %s Wertungen: %d" % (str(self.start_time), str(self.creation_date), self.runs.count())

    @classmethod
    def current(cls, version=None):
        if version is None:
            version = Version.current_active()
        if version is None:
            return None
        return cls.objects.filter(version=version.id)


    @classmethod
    def for_birth(cls, birth_date, gender):
        current_starts = cls.current()
        current_version = Version.current_active()
        if current_version is None:
            return None
        age_group = AgeGroup.select_from_birth_qry(birth_date, gender,
                                               datetime.datetime.combine(current_version.date, datetime.time()))

        runs = Run.objects.filter(possible_ages__in=age_group)
        return current_starts.filter(runs__in=runs).all()



class Version(models.Model):
    class Meta:
        ordering = ["-date"]

    date = models.DateField(verbose_name=u"Veranstaltungsdatum")
    net_end = models.DateField(verbose_name=u"Meldeschluss(Netz)")
    starts = models.ManyToManyField(Start, verbose_name=u"Zugeordnete Starts")

    def _sub_date(self, diff):
        return self.date - datetime.timedelta(days=diff)

    def __unicode__(self):
        return u" %d Windberglauf (%s)" % (self.number, unicode(self.date))

    @property
    def number(self):
        return self.date.year - 1950

    @staticmethod
    def current_active():
        try:
            return Version.objects.latest('date')
        except Version.DoesNotExist:
            return None

    @staticmethod
    def current_active_id():
        latest = Version.current_active()

        if latest is None:
            return None
        return latest.id

    @staticmethod
    def by_year(year):
        """Find a specific version by year.

        It returns None if none found.

        :param year: The year (as int) to search for.
        :type year: int
        :rtype: Version or None
        :return: The version or none.
        """
        search_start = datetime.date(year=year, month=1, day=1)
        search_end = datetime.date(year=year, month=12, day=31)
        qry = Version.objects.filter(date__gte=search_start, date__lte=search_end)
        try:
            return qry.get()
        except Version.MultipleObjectsReturned or Version.DoesNotExist:
            return None


class SimpleNameModelMixin(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    @classmethod
    def get_or_create(cls, name):
        try:
            return cls.objects.filter(name__iexact=name).all()[0:1].get()
        except cls.DoesNotExist:
            return cls.objects.create(name=name)


class Club(SimpleNameModelMixin):
    pass

    def __unicode__(self):
        return "Club: %s" % self.name


class Starter(models.Model):
    GENDER_CHOICES = (
        ("M", u"männlich"),
        ("F", u"weiblich")
    )

    name = models.CharField(verbose_name=u"Name", max_length=200)
    given = models.CharField(verbose_name=u"Vorname", max_length=200)
    birth = models.DateField(verbose_name=u"Geburtsdatum")
    club = models.ForeignKey(Club, verbose_name=u"Verein")
    gender = models.CharField(verbose_name=u"Geschlecht", max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(verbose_name=u"E-Mail", blank=True)
    comment = models.TextField(verbose_name=u"Anmerkungen", blank=True)
    runs = models.ManyToManyField(Run, verbose_name=u"Starts")
    version = models.ForeignKey(Version, default=Version.current_active_id, related_name="starters")

    def get_age_groups(self, for_date):
        return AgeGroup.select_from_birth(self.birth, self.gender, for_date)

    def actual_age_group(self):
        return AgeGroup.select_from_birth_qry(self.birth, self.gender, self.version.date).filter(is_pseudo=False).get()
    actual_age_group.short_description = u"Ak"

    def __unicode__(self):
        return u"%s, %s - %s (%s)" % (self.name, self.given, self.email, self.comment)
