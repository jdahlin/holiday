from xml.etree.ElementTree import tostring, Element, ElementTree, SubElement

from holiday.main.models import Country, Holiday


class XMLDatabaseSerializer:
    def serialize(self):
        node = Element('root')
        self._doHolidays(node)
        self._doCountries(node)
        return tostring(node)
    
    def _doCountries(self, parent):
        node = SubElement(parent, 'countries')
        for country in Country.objects.all():
            self._doCountry(node, country)
        
    def _doCountry(self, parent, country):
        node = SubElement(parent, 'country', attrib=dict(
            name=country.name))
        if len(country.states):
            self._doStates(node, country.states)
        self._doCelebrates(node, country.holidays)
            
    def _doStates(self, parent, states):
        node = SubElement(parent, 'states')
        for state in states:
            self._doState(node, state)
            
    def _doState(self, parent, state):
        node = SubElement(parent, 'state', attrib=dict(name=state.name))
        self._doCelebrates(node, state.holidays)
        
    def _doCelebrates(self, parent, holidays):
        node = SubElement(parent, 'celebrates')
        for holiday in holidays:
            self._doCelebrate(node, holiday)
            
    def _doCelebrate(self, parent, holiday):
        SubElement(parent, 'celebrate', attrib=dict(holiday=str(holiday.id)))
    
    def _doHolidays(self, parent):
        node = SubElement(parent, 'holidays')
        for holiday in Holiday.objects.all():
            self._doHoliday(node, holiday)

    def _doHoliday(self, parent, holiday):
        node = SubElement(parent, 'holiday', 
                          attrib=dict(name=holiday.name,
                                      id=str(holiday.id)))
        if holiday.definition:
            node.attrib['definition'] = holiday.definition
        else:
            node.attrib['month'] = str(holiday.month)
            node.attrib['day'] = str(holiday.day)


class XMLDatabaseDeserializer:
    def deserialize(self, string):
        root = parse(string)
        self._doHolidays(root.findall('holidays/holiday'))
        self._doCountries(root.findall('countries/country'))
    
    def _doCountry(self, nodes):
        for node in nodes:
            country = Country()
            country.name = node.attrib['name']
            self._doStates(node, country)
            self._doCelebrates(node, country=country)
            country.save()

    def _doStates(self, parent, country):
        for node in parent.findall('states/state'):
            state = State()
            state.name = node.attrib['name']
            state.country = country
            self._doCelebrates(node, state=state)
            state.save()

    def _doCelebrates(self, parent, country=None, state=None):
        for node in parent.findall('celebrates/celebrate'):
            holiday = Holiday.get(node.id)
            if country:
                holiday.country = country
            if state:
                holiday.state = state
            holiday.save()

    def _doHolidays(self, nodes):
        for node in nodes:
            holiday = Holiday()
            holiday.id = int(node.attrib['id'])
            holiday.name = node.attrib['name']
            if 'definition' in node.attrib:
                holiday.definition = definition
            else:
                holiday.month = int(node.attrib['month'])
                holiday.day = int(node.attrib['day'])
            holiday.save()

