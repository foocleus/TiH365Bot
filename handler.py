from random import randint
#import asyncio
from aiogram import Dispatcher
#from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType
from aiogram.types.callback_query import CallbackQuery

from stores import CommandStore, KeyboardStore, ButtonStore, CallbackStore
import stores.StringStore as Strs
import DataManager

dp = Dispatcher()

# Handle callbacks
@dp.callback_query()
async def handleCallback(callbackQuery: CallbackQuery):
    userId = callbackQuery.from_user.id
    Strs.setLocaleById(userId)
    KeyboardStore.refreshLocale()
    if callbackQuery.message.content_type == ContentType.TEXT:
        if callbackQuery.data[:4] != "lang":
            match callbackQuery.data:
                case CallbackStore.ECHO_UPPER:
                    await callbackQuery.message.edit_text(callbackQuery.message.text.upper())
                case CallbackStore.ECHO_CAPITALIZE:
                    await callbackQuery.message.edit_text(callbackQuery.message.text.capitalize())

                case CallbackStore.TUTORIAL_FINISH:
                    await callbackQuery.message.edit_reply_markup(None)
                    DataManager.set("isActivated", True, userId)

                case CallbackStore.RESTART_CONTINUE:
                    DataManager.set("isActivated", False, userId)
                    await callbackQuery.message.edit_text("Select your language:", reply_markup=KeyboardStore.inline.language)
                case CallbackStore.RESTART_CANCEL:
                    await callbackQuery.message.delete()

                case CallbackStore.PREFERENCES_LANGUAGE:
                    await callbackQuery.message.edit_text("Select your language:", reply_markup=KeyboardStore.inline.language)
                case _:
                    await callbackQuery.answer(Strs.get(Strs.ERR_SOMETHING_WRONG))
        else:
            language = callbackQuery.data[4:]
            if not DataManager.get("isActivated", userId): # User sets language using /start
                DataManager.upsertUser(userId, language)
                Strs.setLocaleById(userId)
                KeyboardStore.refreshLocale()
                await callbackQuery.message.edit_text(Strs.get(Strs.INF_HELP_HEADER)
                                                       + CommandStore.listCommandInfo()
                                                       + Strs.get(Strs.INF_TUTOR_NOTICE), 
                                                      reply_markup=KeyboardStore.inline.tutorial)
            else:                                           # User sets language using preferences menu
                DataManager.set("lang", language, userId)
                Strs.setLocaleById(userId)
                KeyboardStore.refreshLocale()
                await callbackQuery.message.edit_text(getPreferencesRaw(userId), reply_markup=KeyboardStore.inline.preferences)

# Handle commands
@dp.message(lambda message: message.content_type == ContentType.TEXT and message.text.startswith('/'))
async def handleCommand(message: Message):
    userId = message.from_user.id
    isActivated = DataManager.get("isActivated", userId)
    Strs.setLocaleById(userId)
    KeyboardStore.refreshLocale()
    if message.content_type == ContentType.TEXT:
        if not isActivated and message.text[1:] != CommandStore.START.command:
            await message.answer("Finish setup before using the bot functionality") 
            return 
        match message.text[1:]:
            case CommandStore.START.command:
                if isActivated: 
                    await message.answer(Strs.get(Strs.PRO_RESTART), reply_markup=KeyboardStore.inline.restart)
                else:
                    await message.answer("Select your language:", reply_markup=KeyboardStore.inline.language)
            case CommandStore.HELP.command:
                await message.answer(Strs.get(Strs.INF_HELP_HEADER) + CommandStore.listCommandInfo())
            case CommandStore.RND.command:
                await message.answer(str(randint(0, 255)), reply_markup=KeyboardStore.reply.rndCommand)
            case CommandStore.PREFERENCES.command | CommandStore.PREF.command:
                await message.answer(getPreferencesRaw(userId), reply_markup=KeyboardStore.inline.preferences)
            case _:
                await message.answer(Strs.get(Strs.ERR_COMMAND_NOT_EXIST))


# Handle message
@dp.message()
async def handleText(message: Message):
    userId = message.from_user.id
    Strs.setLocaleById(userId)
    KeyboardStore.refreshLocale()
    if message.content_type == ContentType.TEXT:
        if not DataManager.get("isActivated", userId):
            message.answer("Finish setup before using the bot functionality") 
            return 
        match message.text:
            case ButtonStore.reply.askLargerNum.text:
                await message.answer(str(randint(0, 255*255)))
            case _:
                await message.send_copy(userId, reply_markup=KeyboardStore.inline.echo)
    else:
        await message.answer(Strs.get(Strs.ERR_NOT_TEXT_INPUT))


def getPreferencesRaw(userId) -> str:
    return f'''
            {Strs.get(Strs.INF_PREFERENCES)}
            {Strs.get(Strs.PRF_LANGUAGE)} - <code>{DataManager.get("lang", userId)}</code>
            ''' 
