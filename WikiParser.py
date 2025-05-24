import wikipedia
from random import sample

from month_full_names import *
from logger import Logger


CONTENT_START_INDEX = 1
CONTENT_END_INDEX = 5
SECTION_SPLITTER = "\n\n\n== "
RANGE_SPLITTER = "\n\n\n=== "

EVENTS = "Events =="
BIRTHS = "Births =="
DEATHS = "Deaths =="
HOLIDAYS = "Holidays and observances =="

WIKIPEDIA_HYPERLINK = "https://en.wikipedia.org/wiki/"

headers = {
    "Events ==" : "\n<b>Historical events that happened today:</b>",
    "Births ==" : "\n<b>Famous people born today:</b>",
    "Deaths ==" : "\n<b>Famous people who passed away today:</b>",
    "Holidays and observances ==" : "\n<b>Holidays around the globe today:</b>",
}
filters = [
    "Christian feast day:"
]

RANGES = ["=== Pre-1600 ===", "=== 1601-1900 ===", "=== 1901_Present ==="]


def setLanguage(lang):
    pass

def getPage(date : str): 
    try: 
        day, month = date.split(".")
        day, month = int(day), int(month)
        return wikipedia.page(f"{months_full_names[month]} {day}", auto_suggest=False)
    except:
        return False

def getTodayPage():
    return getPage(wikipedia.datetime.now().strftime("%d.%m"))

def getPageEvents(page, selectedSections, entriesPerRange, holidaysEntries):
    message = ""
    def splitContent(content : str):
        sectionsRaw = content.split(SECTION_SPLITTER)
        sectionsRaw = sectionsRaw[CONTENT_START_INDEX : CONTENT_END_INDEX]
        sectionsFinal = []
        for section in sectionsRaw:
            if not section[:section.find("\n")] in selectedSections:
                continue

            sectionName = headers[section[:section.find("\n")]]
            rangesStartIndex = section.find("\n")

            if section[:rangesStartIndex] == HOLIDAYS:        
                sectionsFinal.append(sectionName + section[rangesStartIndex+1:])
            else:
                sectionsFinal.append(sectionName + section[rangesStartIndex+3:]) 
        return sectionsFinal
    
    def splitSection(content : str):
        rangesRaw = content.split(RANGE_SPLITTER)
        rangesFinal = []
        for range in rangesRaw:
            entriesStartIndex = range.find("\n")
            rangesFinal.append(range[entriesStartIndex+1:])
        return rangesFinal
    
    def splitRanges(section):
        return section.split("\n")
    
    def filterEntries(entries):
        for filter in filters:
            while entries.count(filter) > 0:
                entries.remove(filter)
        return entries
    
    def sortEntries(entries):
        def safeIntSort(iterable):
            filtered = [value for value in iterable if value.isdecimal()]
            return sorted(filtered, key=int)
         
        years = []
        sortedEntries = []
        for entry in entries:
            years.append(entry[:entry.find(" ")])
        years = safeIntSort(years)
        for year in years:
            for entry in entries:
                if entry.find(year) > -1:
                    sortedEntries.append(entry)
                    entries.remove(entry)
                    break
        return sortedEntries
    
    def addLinksToEntries(entries):
        entriesFinal = []
        for entry in entries:
            try:
                nameStartIndex = entry.find(" – ")+3
                nameEndIndex = entry.find(", ", nameStartIndex)
                name = entry[nameStartIndex:nameEndIndex]
                url = WIKIPEDIA_HYPERLINK + name
            except:
                entriesFinal.append(entry)
            else:
                entriesFinal.append(entry[:nameStartIndex] + f"<a href=\"{url}\">" + name + "</a>" + entry[nameEndIndex:]) 

        return entriesFinal
    
    def safeSample(values, number):
        if len(values) <= number:
            return values
        else:
            return sample(values, number)

    for section in splitContent(page.content):
        headerEndIndex = section.find("/b>")+3
        message += section[:headerEndIndex]
        section = section[headerEndIndex:]
        ri = 0 # range index
        for range in splitSection(section):
            entries = filterEntries(splitRanges(range))
            if headerEndIndex == len(headers["Events =="]):
                message += "\n" + "\n".join(sortEntries(safeSample(entries, entriesPerRange[ri])))
            elif headerEndIndex == len(headers["Holidays and observances =="]):
                message += "\n" + "\n".join(safeSample(entries, holidaysEntries))
            else:
                message += "\n" + "\n".join(addLinksToEntries(sortEntries(safeSample(entries, entriesPerRange[ri]))))
            message += "\n"
            ri += 1

    message += f"\n🔗 Source: <a href=\"{page.url}\">Wikipedia</a>"
    return message

def getDayEvents(date, selectedSections, entriesPerRange, holidaysEntries):
    return getPageEvents(getPage(date), selectedSections, entriesPerRange, holidaysEntries)

def getTodayEvents(selectedSections, entriesPerRange, holidaysEntries):
    return getDayEvents(wikipedia.datetime.now().strftime("%d.%m"), selectedSections, entriesPerRange, holidaysEntries)

#getTodayEvents([EVENTS, BIRTHS, DEATHS, HOLIDAYS], [2, 8, 2], 5)