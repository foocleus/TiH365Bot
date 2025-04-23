import wikipedia
from random import sample

from month_full_names import *
from logger import Logger


CONTENT_START_INDEX = 1
CONTENT_END_INDEX = 5

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

def getDayEvents(date, selectedSections, entriesPerRange, holidaysEntries):
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
        sectionsRaw = sectionsRaw[CONTENT_START_INDEX : CONTENT_END_INDEX]
        sectionsFinal = []
        for section in sectionsRaw:
            if not section[:section.find('\n')] in selectedSections:
                continue

            sectionName = headers[section[:section.find('\n')]]
            rangesStartIndex = section.find('\n')

            if section[:rangesStartIndex] == HOLIDAYS:        
                sectionsFinal.append(sectionName + section[rangesStartIndex+1:])
            else:
                sectionsFinal.append(sectionName + section[rangesStartIndex+3:]) 
        return sectionsFinal
    
    def splitSection(content : str):
        rangesRaw = content.split("\n\n\n=== ")
        rangesFinal = []
        for range in rangesRaw:
            entriesStartIndex = range.find('\n')+1
            rangesFinal.append(range[entriesStartIndex:])
        return rangesFinal
    
    def splitEntries(section):
        return section.split('\n')
    
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
                    break
        return sortedEntries
    
    def addLinksToEntries(entries):
        entriesFinal = []
        for entry in entries:
            try:
                nameStartIndex = entry.find(" – ")+3
                nameEndIndex = entry.find(", ", nameStartIndex)
                name = entry[nameStartIndex:nameEndIndex]
                url = f"https://en.wikipedia.org/wiki/{name}"
            except:
                entriesFinal.append(entry)
            else:
                entriesFinal.append(entry[:nameStartIndex] + f'<a href="{url}">' + name + '</a>' + entry[nameEndIndex:]) 

        return entriesFinal

    page = getPage(date)
    for section in splitContent(page.content):
        headerEndIndex = section.find('/b>')+3
        message += section[:headerEndIndex]
        section = section[headerEndIndex:]
        ri = 0 # range index
        for range in splitSection(section):
            entries = splitEntries(range)
            if len(entries) <= entriesPerRange[ri]:
                message += "\n".join(entries)
            else:
                if headerEndIndex == len(headers["Events =="]):
                    message += "\n" + "\n".join(sortEntries(sample(entries, entriesPerRange[ri])))
                elif headerEndIndex == len(headers["Holidays and observances =="]):
                    message += "\n" + "\n".join(sample(entries, holidaysEntries))
                else:
                    message += "\n" + "\n".join(addLinksToEntries(sortEntries(sample(entries, entriesPerRange[ri]))))
            message += "\n"
            ri += 1

    message += f"\n🔗 Soruce: <a href=\"{page.url}\">Wikipedia</a>"
    return message

def getTodayEvents(selectedSections, entriesPerRange, holidaysEntries):
    return getDayEvents(wikipedia.datetime.now().strftime("%m.%d"), selectedSections, entriesPerRange, holidaysEntries)

#getTodayEvents([EVENTS, BIRTHS, DEATHS, HOLIDAYS], [2, 8, 2], 5)