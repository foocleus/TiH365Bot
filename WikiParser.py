import wikipedia
from random import sample

from month_full_names import *
from logger import Logger

EVENTS = "Events =="
BIRTHS = "Births =="
DEATHS = "Deaths =="
HOLIDAYS = "Holidays and observances =="

headers = {
    "Events ==" : "\n<b>Historical events that happened today:</b>",
    "Births ==" : "\n<b>Famous people born today:</b>",
    "Deaths ==" : "\n<b>Famous people who passed away today:</b>",
    "Holidays and observances ==" : "\n<b>Holidays around the globe today:</b>",
}

RANGES = ["=== Pre-1600 ===", "=== 1601-1900 ===", "=== 1901_Present ==="]


def setLanguage(lang):
    pass

def getDayEvents(date, selectedSections, rangesCount):
    message = ""
    def getPage(date : str): 
        month, day = date.split('.')
        month, day = int(month), int(day)
        try: 
            return wikipedia.page(f"{months_full_names[month]} {day}", auto_suggest=False)
        except Exception.__name__ as ename:
            Logger.error(ename)
    
    def splitContent(content : str):
        sectionsRaw = content.split("\n\n\n== ")
        sectionsRaw = sectionsRaw[1:5]                          # cut off all sections, except list of dates
        sectionsFinal = []
        for section in sectionsRaw:
            if not section[:section.find('\n')] in selectedSections:
                continue

            sectionName = headers[section[:section.find('\n')]]

            if section[:section.find('\n')] == HOLIDAYS:        # delete remaining of section header
                sectionsFinal.append(sectionName + section[section.find('\n'):])
            else:
                sectionsFinal.append(sectionName + section[section.find('\n')+3:]) 
        return sectionsFinal
    
    def splitSection(content : str):
        sectionsRaw = content.split("\n\n\n=== ")
        sectionsFinal = []
        for section in sectionsRaw:
            sectionsFinal.append(section[section.find('\n')+1:]) # delete remaining of section header
        return sectionsFinal
    
    def splitEntries(section):
        return section.split('\n')

    for section in splitContent(getPage(date).content):
        message += section[:section.find('/b>')+3]
        section = section[section.find('/b>')+3:]
        for range in splitSection(section):
            entries = splitEntries(range)
            if len(entries) < 3:
                message += "\n".join(entries)
            else:
                message += "\n" + "\n".join(sample(entries, 3))
        message += "\n"

    print(message)
    
    pass

def getTodayEvents(selectedSections, rangesCount):
    return getDayEvents(wikipedia.datetime.now().strftime("%m.%d"), selectedSections, rangesCount)

getTodayEvents([BIRTHS, DEATHS], [2, 8, 2])