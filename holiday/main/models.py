import datetime

from django.db.models import Model
from django.db.models import (CharField, DateField, ForeignKey, IntegerField,
                              ManyToManyField)

from holiday.definition import DefinitionParser
from holiday.utils import formatday, formatmonth


class Country(Model):
    name = CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u'<Country "%s">' % (self.name,)
    
    @property
    def states(self):
        return State.objects.all().filter(country=self)
    
    @property
    def holidays(self):
        return Holiday.objects.all().filter(country=self)
        
        
class State(Model):
    name = CharField(max_length=50)
    country = ForeignKey(Country)
    
    def __unicode__(self):
        return u'<State "%s" in "%s">' % (self.name, self.country.name)

    @property
    def holidays(self):
        return Holiday.objects.all().filter(state=self)


MONTHS_CHOICES = [(0, 'Not fixed')] + [(i, formatmonth(i)) for i in range(1, 13)]
DAY_CHOICES = [(0, 'Not fixed')] + [(i, formatday(i)) for i in range(1, 32)]

class Holiday(Model):
    name = CharField(max_length=50)
    definition = CharField(max_length=100, blank=True)
    month = IntegerField(default=0, choices=MONTHS_CHOICES)
    day = IntegerField(default=0, choices=DAY_CHOICES)
    country = ManyToManyField(Country, blank=True, null=True)
    state = ManyToManyField(State, blank=True, null=True)
    
    def __unicode__(self):
        return u'<Holiday "%s">' % (self.name,)
        
    def getByCountryAndYear(self, countryName, year):    
        country = Country.objects.get(name=countryName)
        return Holiday.objects.all().filter(country=country)
    
    def getDateByYear(self, year):
        if self.definition:
            return DefinitionParser().parse(self.definition)(year)
        else:
            return datetime.date(year, self.month, self.day)

