import wikipedia
from random import sample
from copy import deepcopy

import cacher
from translator import translator
from month_full_names import *
from logger import Logger


CONTENT_START_INDEX = 1
CONTENT_END_INDEX = 5
SECTION_SPLITTER = "\n\n\n== "
RANGE_SPLITTER = "\n\n\n=== "
EXISTING_DATE_LIST_LEN = 10

EVENTS = "Events"
BIRTHS = "Births"
DEATHS = "Deaths"
HOLIDAYS = "Holidays and observances"

WIKIPEDIA_HYPERLINK = "https://en.wikipedia.org/wiki/"

sectionTypes = [EVENTS, BIRTHS, DEATHS, HOLIDAYS]

headers = {
    EVENTS : "\n<b>Historical events that happened today:</b>",
    BIRTHS : "\n<b>Famous people born today:</b>",
    DEATHS : "\n<b>Famous people who passed away today:</b>",
    HOLIDAYS : "\n<b>Holidays around the globe today:</b>",
}
filters = [
    "Christian feast day:"
]

#RANGES = ["=== Pre-1600 ===", "=== 1601-1900 ===", "=== 1901_Present ==="]


def setLanguage(lang):
    pass

def convertToPageName(date):
    day, month = date.split(".")
    day, month = int(day), int(month)
    return f"{months_full_names[month]} {day}"

def getPage(date : str): 
    try: 
        return wikipedia.page(convertToPageName(date), auto_suggest=False)
    except:
        return False

def getTodayDate():
    return wikipedia.datetime.now().strftime("%d.%m")

def getTodayPage():
    return getPage(getTodayDate())

async def getPageEvents(page, selectedSections, entriesPerRange, holidaysEntries, language):
    message = ""
    def splitPageContent(content):
        content = content.replace('"', '&quot;')
        sections = content.split(SECTION_SPLITTER)
        sections = sections[CONTENT_START_INDEX : CONTENT_END_INDEX]
        return sections

    def filterAndHeaderCached(cachedContent):
        processedContent = {}
        for name, section in cachedContent.items():
            if not name in selectedSections:
                continue

            section.append(headers[name])
            processedContent[name] = section 
        return processedContent
    
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
                if nameEndIndex < 0:
                    nameEndIndex = entry.find(" (", nameStartIndex)
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

    
    cachedContend = cacher.deserializePageContent(page.original_title, language)
    if not cachedContend:
        untranslatedList = []
        for i, section in enumerate(splitPageContent(page.content)):
            section = section[section.find(RANGE_SPLITTER)+len(RANGE_SPLITTER):]
            cachedContend[sectionTypes[i]] = list()
            for range in splitSection(section):
                untranslatedList.append(range)

        if len(untranslatedList) == EXISTING_DATE_LIST_LEN:
            if language != "en":
                responses = await translator.translate(untranslatedList, language, "en")
                ranges = [response.text for response in responses]
            else:
                ranges = deepcopy(untranslatedList)
            for i, range in enumerate(ranges):
                cachedContend[sectionTypes[i // 3]].append(range)
        else:
            cachedContend = {}
        cacher.serializePageContent(cachedContend, page.original_title, language)

    cachedContend = filterAndHeaderCached(cachedContend)
    for name, section in cachedContend.items():
        message += section.pop()
        for i, range in enumerate(section):
            entries = filterEntries(splitRanges(range))
            if name == EVENTS:
                message += "\n" + "\n".join(sortEntries(safeSample(entries, entriesPerRange[i])))
            elif name == HOLIDAYS:
                message += "\n" + "\n".join(safeSample(entries, holidaysEntries))
            else:
                message += "\n" + "\n".join(addLinksToEntries(sortEntries(safeSample(entries, entriesPerRange[i]))))
            message += "\n"

    message += f"\n🔗 Source: <a href=\"{page.url}\">Wikipedia</a>"
    return message

async def getDayEvents(date, selectedSections, entriesPerRange, holidaysEntries, language):
    return await getPageEvents(getPage(date), selectedSections, entriesPerRange, holidaysEntries, language)

async def getTodayEvents(selectedSections, entriesPerRange, holidaysEntries, language):
    return await getDayEvents(wikipedia.datetime.now().strftime("%d.%m"), selectedSections, entriesPerRange, holidaysEntries, language)

#getTodayEvents([EVENTS, BIRTHS, DEATHS, HOLIDAYS], [2, 8, 2], 5)