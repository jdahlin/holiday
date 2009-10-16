from dateutil.easter import easter

algorithms = {}

def gregorian_easter(year):
    return easter(year)
algorithms['EASTER'] = gregorian_easter



