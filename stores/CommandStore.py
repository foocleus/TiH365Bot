from aiogram.types import BotCommand

import stores.StringStore as Strs

START = BotCommand(command="start", description=Strs.COM_START)
HELP = BotCommand(command="help", description=Strs.COM_HELP)
RND = BotCommand(command="rnd", description=Strs.COM_RND)
PREFERENCES = BotCommand(command="preferences", description=Strs.COM_PREFERENCES)
PREF = BotCommand(command="pref", description=Strs.COM_PREFERENCES)

__copy = locals().copy()

def listCommandInfo():
    commandInfoList = ""
    for varname, command in __copy.items():
       if varname.isupper():
           commandInfoList += f"/{command.command} - {Strs.get(command.description)}\n"
    return commandInfoList

