import datetime
import operator

from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context

from holiday.databaseserializer import XMLDatabaseSerializer
from holiday.main.models import Country, Holiday
from holiday.utils import formatday, formatmonth


def index(request):
    return render_to_response('index.html') 
    
def html_index(request):
    date = datetime.date.today()
    return html(request, date.year)
    
def html(request, year=None):
    result = []
    year = int(year)
    holidays = Holiday.objects.all()
    for holiday in holidays:
        date = holiday.getDateByYear(year)
        datestring = '%s %s' % (formatmonth(date.month),
                                formatday(date.day))      
        countries = [c.name for c in holiday.country.all().order_by('name')]
        result.append(dict(name=holiday.name, rawdate=date, date=datestring, 
                           countries=', '.join(countries)))
    result = sorted(result, key=operator.itemgetter('rawdate'))
    return render_to_response('holidays.html', 
                              dict(holidays=result,
                                   thisyear=year,
                                   years=range(year-3, year+3)))

def ics(request):
    countryName = 'Brazil'
    timezone = 'BRST'
    year = 2009

    result = []
    for holiday in Holiday.getByCountryAndYear(countryName, year):
        startdate = holiday.getDateByYear(year)
        enddate = startdate + relativedelta(days=1)      
        result.append(dict(name=holiday.name, 
                           timezone=timezone,
                           startdate=startdate.strftime('%Y%m%d'),
                           enddate=enddate.strftime('%Y%m%d')))
    response = HttpResponse(mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.ics' % (countryName, year)
    
    t = loader.get_template('holidays.ics')
    c = Context(dict(holidays=result,
                year=year, 
                daylight=False))

    response.write(t.render(c))
    return response

def xml(request):
    response = HttpResponse(mimetype='text/plain')
    response.write(XMLDatabaseSerializer().serialize())
    return response

