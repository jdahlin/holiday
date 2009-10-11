from django.db.models import Model
from django.db.models import CharField, DateField, ForeignKey, IntegerField


class Country(Model):
    name = CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u'<Country "%s">' % (self.name,)
    

class State(Model):
    name = CharField(max_length=50)
    country = ForeignKey(Country)
    
    def __unicode__(self):
        return u'<State "%s" in "%s">' % (self.name, self.country.name)


MONTHS_CHOICES = [
    (0, 'Not fixed'),
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]

DAY_CHOICES = [
    (0, 'Not fixed')
] + [(i, str(i)) for i in range(1, 32)]


class Holiday(Model):
    name = CharField(max_length=50)
    month = IntegerField(default=0, choices=MONTHS_CHOICES)
    day = IntegerField(default=0, choices=DAY_CHOICES)
    country = ForeignKey(Country, blank=True, null=True)
    state = ForeignKey(State, blank=True, null=True)
    
