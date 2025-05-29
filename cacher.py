import os

CACHE_PATH = "./cache"


def loadCachedText(date, language):
    path = f"{CACHE_PATH}/{language}/{date}"
    os.makedirs(path, exist_ok=True)
    textDict = {}
    for sectionFolder in os.listdir(path):
        textDict[sectionFolder] = list()
        for rangeFile in os.listdir(f"{path}/{sectionFolder}"):
            filePath = f"{path}/{sectionFolder}/{rangeFile}"
            with open(filePath, "r") as cacheFile:
                textDict[sectionFolder].append(cacheFile.read())
    return textDict        

def writeTextToCache(textDict, date, language):
    for sectionEndIndex, rangeList in textDict.items():
        path = f"{CACHE_PATH}/{language}/{date}/{sectionEndIndex}"
        os.makedirs(path, exist_ok=True)
        i = 0
        for text in rangeList:
            with open(f"{path}/{i}", "w") as cacheFile:
                cacheFile.write(text)
            i += 1