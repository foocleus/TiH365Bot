import wikipedia
from random import sample

from month_full_names import *
from logger import Logger

EVENTS = "== Events =="
BIRTHS = "== Births =="
DEATHS = "== Deaths =="
HOLIDAYS = "== Holidays and observances =="

PRE_1600 = "=== Pre-1600 ==="
Y1601_1900 = "=== 1601-1900 ==="
Y1901_PRESENT = "=== 1901_Present ==="


def setLanguage(lang):
    pass

def getDayEvents(date, sections, ranges, entriesPerRange):
    SECTION_SPLITTER = "\n\n\n== "
    RANGE_SPLITTER = "\n\n\n=== "

    message = ""
    def getPage(date : str): 
        month, day = date.split('.')
        month, day = int(month), int(day)
        try: 
            return wikipedia.page(f"{months_full_names[month]}_{day}")
        except Exception.__name__ as ename:
            Logger.error(ename)
    
    def splitContent(content : str, splitter):
        sectionsRaw = content.split(splitter)
        if splitter == SECTION_SPLITTER: 
            sectionsRaw = sectionsRaw[1:5] # cut off everything, except list of dates
        sectionsFinal = []
        for section in sectionsRaw:
            sectionsFinal.append(section[section.find('\n')+3:]) # delete remainings of section header
        return sectionsFinal
    
    def splitEntries(section):
        return section.split('\n')

    for section in splitContent(getPage(date).content, SECTION_SPLITTER):
        for range in splitContent(section, RANGE_SPLITTER):
            entries = splitEntries(range)
            if len(entries) < entriesPerRange:
                message += "\n".join(entries)
            else:
                message += "\n" + "\n".join(sample(entries, entriesPerRange))
        
    print(message)
    
    pass

def getTodayEvents(sections, ranges, entriesPerRange):
    return getDayEvents(wikipedia.datetime.now().strftime("%m.%d"), sections, ranges, entriesPerRange)

getTodayEvents([EVENTS, BIRTHS, DEATHS, HOLIDAYS], [PRE_1600, Y1601_1900, Y1901_PRESENT], 3)