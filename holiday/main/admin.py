from holiday.main.models import Country, State, Holiday
from django.contrib.admin import site, ModelAdmin


class CountryAdmin(ModelAdmin):
    fieldsets = [
        ('Name of Country', {'fields': ['name']}),
    ]
    list_display = ['name']
    admin_order_field = 'name'

    
site.register(Country, CountryAdmin)


site.register(State)

class HolidayAdmin(ModelAdmin):
    list_display = ['name', 'definition', 'month', 'day']
    admin_order_field = 'name'

site.register(Holiday, HolidayAdmin)

