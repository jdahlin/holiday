import datetime
import operator

from dateutil.relativedelta import relativedelta

from holiday.datealgorithms import algorithms
from holiday.utils import parseweekday

#
# variable operator offset
# 
# variable is either:
# - an algorithm (eg, EASTER)
# - a month in MM format (january => 01)
# - a date in MM-YY format (1st of jan => 01-01)
# 
# operator is either:
# - plus/+ after
# - minus/- before
#
# offset is either:
# - number
# - weekday (monday, tuesday etc)
# - weekday multiplier, 3rd monday = MONDAY(3)
#
# Examples:
#  Good Friday = EASTER - 2
#  Midsummer   = 06-20 + SATURDAY
#  MLK day     = 01 + MONDAY(3)

class DefinitionParser:
    def __init__(self):
        self._args = []

    def parse(self, definition):
        parts = definition.split()
        
        opfunc = None
        days = 0
        weekday = None
        if len(parts) == 1:
            pass    
        elif len(parts) == 3:
            # operator
            opstring = parts[1]
            if opstring in ['+', 'plus']:
                opfunc = operator.__add__
            elif opstring in ['-', 'minus']:
                opfunc = operator.__sub__
            else:
                raise ValueError("Unsupported operator: " + repr(opstring))
        
            # number
            delta = parts[2]
            try:
                days = int(delta)
            except ValueError:
                weekday, offset = parseweekday(delta)
                if offset != 0:
                    weekday = weekday.__call__(offset)
        else:
            raise ValueError("%s is not a valid definition." % (definition,))
        
        # date variable
        variable = parts[0]

        if variable in algorithms:
            datefunc = algorithms.get(variable)
        elif len(variable) == 2:
            month = int(variable[:2])
            datefunc = lambda year: datetime.date(year, month, 1)
        elif len(variable) == 5 and variable[2] == '-':
            month = int(variable[:2])
            day = int(variable[3:5])
            datefunc = lambda year: datetime.date(year, month, day)
        else:
            raise ValueError("Invalid date variable: " + variable)
        
        if opfunc is not None and (days != 0 or weekday != None):
            # Wrapper
            days = relativedelta(days=days, weekday=weekday)
            def calc(year):
                return opfunc(datefunc(year), days)
        else:
            calc = datefunc
        return calc
        
if __name__ == '__main__':
    dp = DefinitionParser()
    print dp.parse('EASTER + 50')(2009)
