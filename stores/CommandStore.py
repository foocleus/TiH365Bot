from aiogram.types import BotCommand

import stores.StringStore as Strs

BASIC_COMMANDS = BotCommand(command="", description=Strs.INF_PRIMARY_COMMANDS)
START = BotCommand(command="start", description=Strs.COM_START)
HELP = BotCommand(command="help", description=Strs.COM_HELP)
EVENTSTODAY = BotCommand(command="eventstoday", description=Strs.COM_EVENTSTODAY)
EVENTSTHATDAY = BotCommand(command="eventsthatday", description=Strs.COM_EVENTSTHATDAY)
PREFERENCES = BotCommand(command="preferences", description=Strs.COM_PREFERENCES)

MORE_COMMANDS = BotCommand(command="", description=Strs.INF_SECONDARY_COMMANDS)
LANGUAGE = BotCommand(command="language", description=Strs.COM_LANGUAGE)
SECTIONS = BotCommand(command="sections", description=Strs.COM_SECTIONS)
ENTRIES = BotCommand(command="entries", description=Strs.COM_ENTRIES)
SCHEDULE = BotCommand(command="schedule", description=Strs.COM_SCHEDULE)

__copy = locals().copy()

def listCommandInfo():
    commandInfoList = ""
    for varname, botCommand in __copy.items():
        if varname.isupper():
            if botCommand.command != "":
                commandInfoList += f"/{botCommand.command} - {Strs.get(botCommand.description)}\n"
            else:
                commandInfoList += Strs.get(botCommand.description)
    return commandInfoList

