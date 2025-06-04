from aiogram.types import BotCommand

import stores.StringStore as Strs

START = BotCommand(command="start", description=Strs.COM_START)
HELP = BotCommand(command="help", description=Strs.COM_HELP)
EVENTSTODAY = BotCommand(command="eventstoday", description=Strs.COM_EVENTSTODAY)
EVENTSTHATDAY = BotCommand(command="eventsthatday", description=Strs.COM_EVENTSTHATDAY)
PREFERENCES = BotCommand(command="preferences", description=Strs.COM_PREFERENCES)
PREF = BotCommand(command="pref", description=Strs.COM_PREFERENCES)
LANGUAGE = BotCommand(command="language", description=Strs.COM_LANGUAGE)
SECTIONS = BotCommand(command="sections", description=Strs.COM_SECTIONS)
ENTRIES = BotCommand(command="entries", description=Strs.COM_ENTRIES)
SCHEDULE = BotCommand(command="schedule", description=Strs.COM_SCHEDULE)

__copy = locals().copy()

def listCommandInfo():
    commandInfoList = ""
    for varname, command in __copy.items():
       if varname.isupper():
           commandInfoList += f"/{command.command} - {Strs.get(command.description)}\n"
    return commandInfoList

