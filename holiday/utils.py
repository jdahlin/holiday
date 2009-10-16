from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU 

_MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

_WEEKDAYS = {
    'monday': MO,
    'tuesday': TU,
    'wednesday': WE,
    'thursday': TH,
    'friday': FR,
    'saturday': SA,
    'sunday' : SU
}


def formatday(day):
    daystring = str(day)
    if day < 10 or day > 20:
        if day % 10 == 1:
            return daystring + 'st'
        elif day % 10 == 2:
            return daystring + 'nd'
        elif day % 10 == 3:
            return daystring + 'rd'
    return daystring + 'th'

def formatmonth(month):
    return _MONTHS[month] 

def parseweekday(weekday):
    weekday = weekday.lower()
    if weekday in _WEEKDAYS:
        offset = 0
    elif '(' in weekday and weekday.endswith(')'):
        weekdaypart, offsetpart = weekday[:-1].split('(', 1)
        if not weekdaypart in _WEEKDAYS:
           raise ValueError("Invalid weekday specifier: " + weekday)
        weekday = weekdaypart
        offset = int(offsetpart)
    else:
        raise ValueError("Invalid weekday specifier: " + weekday)        
    return _WEEKDAYS[weekday], offset

