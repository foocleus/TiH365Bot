import asyncio
import json
from os.path import exists
from copy import deepcopy

from logger import logger
from WikiParser import EVENTS, BIRTHS, DEATHS, HOLIDAYS

defaultValues = {
    "lang": "en",
    "isActivated": False,
    "scheduledHour" : 12,
    "selectedSections": [EVENTS, BIRTHS, DEATHS, HOLIDAYS],
    "entriesPerRange": [3, 3, 3],
    "holidaysEntries": 5,
    "currentInput" : None
}
userData = {}
pendingUserIds = []

if not exists("./user-data.json"):
    with open("./user-data.json", "w") as f: f.write("{}")

with open("./user-data.json", "r") as dataFile:
    userData = json.load(dataFile)



def getValue(entry, userId):
    if type(userId) == int: userId = str(userId)
    if not userId in userData:
        return defaultValues[entry]
    return userData[userId].get(entry, defaultValues[entry])
    
def getIdsByValue(entry, value):
    ids = []
    for userId, userValues in userData.items():
        if userValues.get(entry, defaultValues[entry]) == value:
            ids.append(userId)
    return ids

def getAllIds():
    return [userId for userId in userData.keys()]

def set(entry, data, userId):
    if type(userId) == int: userId = str(userId)
    try:
        userData[userId][entry] = data
    except Exception as e:
        print(f"There was an error saving {entry} of user {userId}")
        logger.error(f"There was an error saving {entry} of user {userId}.\n{e}")

def upsertUser(userId:str, language):
    if type(userId) == int: userId = str(userId)
    userData[userId] = deepcopy(defaultValues)
    userData[userId]["lang"] = language
    logger.info(f"Upsert of user {userId} with selected language {language} was handled successfully")

def resetEntry(entry, userId:str):
    userData[userId][entry] = defaultValues[entry]

async def autoSaveTask():
    while True:
        await asyncio.sleep(60) # 60 by default
        with open("./user-data.json", "w") as dataFile:
            json.dump(userData, dataFile, indent=4)
        logger.info("User data auto saved")