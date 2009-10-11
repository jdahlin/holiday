from main.models import Country, State, Holiday

for name in ['Brazil', 'Sweden', 'United States']:
    country = Country(name=name)
    country.save()
 
