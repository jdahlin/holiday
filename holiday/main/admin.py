from holiday.main.models import Country, State, Holiday
from django.contrib.admin import site, ModelAdmin


class CountryAdmin(ModelAdmin):
    fieldsets = [
        ('Name of Country', {'fields': ['name']}),
    ]
    list_display = ['name']
    admin_order_field = 'name'
    verbose_name_plural = 'Countries'
    
site.register(Country, CountryAdmin)


site.register(State)


site.register(Holiday)

