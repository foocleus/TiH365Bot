import os
import asyncio
import json
from copy import deepcopy

from logger import Logger
from WikiParser import EVENTS, BIRTHS, DEATHS, HOLIDAYS

defaultValues = {
    "lang": "EN",
    "isActivated": False,
    "scheduledHour" : 9,
    "selectedSections": [EVENTS, BIRTHS, DEATHS, HOLIDAYS],
    "entriesPerRange": [3, 3, 3],
    "holidaysEntries": 5
}
userData = {}

if not os.path.exists("./user-data.json"):
    with open("./user-data.json", "w") as f: f.write("{}")

with open("./user-data.json", "r") as dataFile:
    userData = json.load(dataFile)



def get(entry, userId):
    if type(userId) == int: userId = str(userId)
    return userData[userId].get(entry, defaultValues[entry])
    
def getIdsByValue(entry, value):
    ids = []
    for userId, userValues in userData.items():
        if userValues.get(entry, defaultValues[entry]) == value:
            ids.append(userId)
    return ids

def set(entry, data, userId):
    if type(userId) == int: userId = str(userId)
    try:
        userData[userId][entry] = data
    except Exception as e:
        print(f"There was an error saving {entry} of user {userId}")
        Logger.error(f"There was an error saving {entry} of user {userId}.\n{e}")

def upsertUser(userId:str, language):
    if type(userId) == int: userId = str(userId)
    userData[userId] = deepcopy(defaultValues)
    userData[userId]["lang"] = language
    Logger.info(f"Upsert of user {userId} with selected language {language} was handled successfully")

def resetEntry(entry, userId:str):
    userData[userId][entry] = defaultValues[entry]

async def autoSaveTask():
    while True:
        await asyncio.sleep(60) # 60 by default
        with open("./user-data.json", "w") as dataFile:
            json.dump(userData, dataFile)
        Logger.info("User data auto saved")