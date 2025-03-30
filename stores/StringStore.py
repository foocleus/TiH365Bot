import json

import DataManager

ERR_SOMETHING_WRONG = "ERR_SOMETHING_WRONG"
ERR_COMMAND_NOT_EXIST = "ERR_COMMAND_NOT_EXIST"
ERR_NOT_TEXT_INPUT = "ERR_NOT_TEXT_INPUT"
BUT_ECHO_UPPER = "BUT_ECHO_UPPER"
BUT_ECHO_CAPITALIZE = "BUT_ECHO_CAPITALIZE"
BUT_TUTOR_FINISH = "BUT_TUTOR_FINISH"
COM_START = "COM_START"
COM_HELP = "COM_HELP"
COM_RND = "COM_RND"
COM_PREFERENCES = "COM_PREFERENCES"
INF_HELP_HEADER = "INF_HELP_HEADER"
INF_TUTOR_NOTICE = "INF_TUTOR_NOTICE"
INF_PREFERENCES = "INF_PREFERENCES"
PRO_RESTART = "PRO_RESTART"
BUT_RESTART_CONTINUE = "BUT_RESTART_CONTINUE"
BUT_RESTART_CANCEL = "BUT_RESTART_CANCEL"
PRF_LANGUAGE = "PRF_LANGUAGE"


selectedLocale = "EN"
locales = {}
with open("./locales.json") as localeFile:
    locales = json.load(localeFile)


def getStringDirectly(stringName, userId:int):
    language = DataManager.get("lang", str(userId))
    return locales[language].get(stringName, "?")

def setLocaleById(userId:int):
    global selectedLocale
    selectedLocale = DataManager.get("lang", str(userId))

def get(stringName):
    return locales[selectedLocale].get(stringName, "?")