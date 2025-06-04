#from random import randint
#import asyncio
#from aiogram.filters import CommandStart, Command
from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from aiogram.types.callback_query import CallbackQuery

from stores import CommandStore, KeyboardStore, CallbackStore
from translator import translator
import stores.StringStore as Strs
import WikiParser
import DataManager


MESSAGE_LENGTH_LIMIT = 4096

PREF_MAIN = "PREF_MAIN"
PREF_LANGUAGE = "PREF_LANGUAGE"
PREF_SECTIONS = "PREF_SECTIONS"
PREF_ENTRIES = "PREF_ENTRIES"
PREF_ENTRIES_INPUT = "PREF_ENTRIES_INPUT"
PREF_TIME_INPUT = "PREF_TIME_INPUT"

dp = Dispatcher()
bot = None

# Handle callbacks
@dp.callback_query()
async def handleCallback(callbackQuery: CallbackQuery):
    userId = callbackQuery.from_user.id
    Strs.setLocaleById(userId)
    KeyboardStore.refreshLocale()
    if callbackQuery.message.content_type == ContentType.TEXT:
        if callbackQuery.data[:4] == "lang":
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
                await callbackQuery.message.edit_text(assembleMenuText(PREF_MAIN, userId), reply_markup=KeyboardStore.inline.preferences)
        elif callbackQuery.data[:6] == "toggle":
            sectionName = callbackQuery.data[6:]
            selectedSections = DataManager.get("selectedSections", userId)
            if selectedSections.count(sectionName) > 0:
                selectedSections.remove(sectionName)
            else:
                selectedSections.append(sectionName)
            DataManager.set("selectedSections", selectedSections, userId)
            await callbackQuery.message.edit_text(assembleMenuText(PREF_SECTIONS, userId), reply_markup=KeyboardStore.inline.preferencesSections)
        elif callbackQuery.data[:5] == "input":
            DataManager.set("currentInput", int(callbackQuery.data[5:]), userId)
            await callbackQuery.message.edit_text(assembleMenuText(PREF_ENTRIES_INPUT, userId))
        else:
            match callbackQuery.data:
                case CallbackStore.TUTORIAL_FINISH:
                    await callbackQuery.message.edit_reply_markup(None)
                    DataManager.set("isActivated", True, userId)
                    await sendLargeText(await WikiParser.getTodayEvents(DataManager.get("selectedSections", userId),
                                                                DataManager.get("entriesPerRange", userId),
                                                                DataManager.get("holidaysEntries", userId), DataManager.get("lang", userId)), callbackQuery.message)
                    
                case CallbackStore.RESTART_CONTINUE:
                    DataManager.set("isActivated", False, userId)
                    await callbackQuery.message.edit_text("Select your language:", reply_markup=KeyboardStore.inline.language)
                case CallbackStore.RESTART_CANCEL:
                    await callbackQuery.message.delete()
                
                case CallbackStore.PREFERENCES_MAIN:
                    await callbackQuery.message.edit_text(assembleMenuText(PREF_MAIN, userId), reply_markup=KeyboardStore.inline.preferences)
                case CallbackStore.PREFERENCES_LANGUAGE:
                    await callbackQuery.message.edit_text("Select your language:", reply_markup=KeyboardStore.inline.language)
                case CallbackStore.PREFERENCES_SECTIONS:
                    await callbackQuery.message.edit_text(assembleMenuText(PREF_SECTIONS, userId), reply_markup=KeyboardStore.inline.preferencesSections)
                case CallbackStore.PREFERENCES_ENTRIES:
                    await callbackQuery.message.edit_text(assembleMenuText(PREF_ENTRIES, userId), reply_markup=KeyboardStore.inline.preferencesEntries)
                case CallbackStore.PREFERENCES_TIME:
                    DataManager.set("currentInput", 4, userId)
                    await callbackQuery.message.edit_text(assembleMenuText(PREF_TIME_INPUT, userId))
                case _:
                    await callbackQuery.answer(Strs.get(Strs.ERR_SOMETHING_WRONG))
            
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
        if DataManager.get("currentInput", userId) is not None:
            await message.answer(Strs.get(Strs.ERR_UNFINISHED_INPUT)) 
            return 
        match message.text[1:]:
            case CommandStore.START.command:
                if isActivated: 
                    await message.answer(Strs.get(Strs.PRO_RESTART), reply_markup=KeyboardStore.inline.restart)
                else:
                    await message.answer("Select your language:", reply_markup=KeyboardStore.inline.language)
            case CommandStore.HELP.command:
                await message.answer(Strs.get(Strs.INF_HELP_HEADER) + CommandStore.listCommandInfo())
            case CommandStore.EVENTSTODAY.command:
                await message.bot.send_chat_action(message.chat.id, "typing")
                await sendLargeText(await WikiParser.getTodayEvents(DataManager.get("selectedSections", userId),
                                                            DataManager.get("entriesPerRange", userId),
                                                            DataManager.get("holidaysEntries", userId), DataManager.get("lang", userId)), message)
            case CommandStore.EVENTSTHATDAY.command:
                await message.answer(Strs.get(Strs.INF_SELECT_DATE))
            case CommandStore.EVENTSTHATDAY.command:
                pass
            case CommandStore.PREFERENCES.command | CommandStore.PREF.command:
                await message.answer(assembleMenuText(PREF_MAIN, userId), reply_markup=KeyboardStore.inline.preferences)
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
        currentInput = DataManager.get("currentInput", userId)
        if currentInput != None:
            try:
                match currentInput:
                    case 0 | 1 | 2:
                        if not message.text.isnumeric(): raise Exception()
                        updatedEntriesPerRange = DataManager.get("entriesPerRange", userId)
                        updatedEntriesPerRange[currentInput] = int(message.text)
                        DataManager.set("entriesPerRange", updatedEntriesPerRange, userId)
                        await message.answer(assembleMenuText(PREF_ENTRIES, userId), reply_markup=KeyboardStore.inline.preferencesEntries)
                    case 3:
                        if not message.text.isnumeric(): raise Exception()
                        DataManager.set("holidaysEntries", int(message.text), userId)
                        await message.answer(assembleMenuText(PREF_ENTRIES, userId), reply_markup=KeyboardStore.inline.preferencesEntries)
                    case 4:
                        if not message.text.isnumeric() or int(message.text) > 23: raise Exception()
                        DataManager.set("scheduledHour", int(message.text), userId)
                        await message.answer(assembleMenuText(PREF_MAIN, userId), reply_markup=KeyboardStore.inline.preferences)
                DataManager.set("currentInput", None, userId)
            except:
                await message.answer(Strs.get(Strs.ERR_INVALID_FORMAT))
            return
        page = WikiParser.getPage(message.text)
        if not page: 
            await message.answer(Strs.get(Strs.ERR_INVALID_DATE)) 
            return
        await message.bot.send_chat_action(message.chat.id, "typing")
        await sendLargeText(await WikiParser.getPageEvents(page,
                                                    DataManager.get("selectedSections", userId),
                                                    DataManager.get("entriesPerRange", userId),
                                                    DataManager.get("holidaysEntries", userId), DataManager.get("lang", userId)), message)
    else:
        await message.answer(Strs.get(Strs.ERR_NOT_TEXT_INPUT))


def setBotClass(botClass):
    global bot
    bot = botClass

async def sendScheduledMessages(userIds):
    page = WikiParser.getTodayPage()
    for id in userIds:
        await sendLargeText(await WikiParser.getPageEvents(page,
                                                     DataManager.get("selectedSections", id),
                                                     DataManager.get("entriesPerRange", id),
                                                     DataManager.get("holidaysEntries", id), DataManager.get("lang", id)), bot, id)


async def sendLargeText(text, messagesClass:Message, userId=0):
    if userId == 0: userId = messagesClass.from_user.id
    language = DataManager.get("lang", userId).lower()
    lastMessageStartIndex = len(text)
    messages = []
    while True:
        fragmentSize = lastMessageStartIndex if lastMessageStartIndex < MESSAGE_LENGTH_LIMIT else MESSAGE_LENGTH_LIMIT
        fragment = text[lastMessageStartIndex - fragmentSize : lastMessageStartIndex]
        charIndex = fragment.find('\n')
        if charIndex > -1:
            messages.append(text[lastMessageStartIndex - fragmentSize + charIndex : lastMessageStartIndex])
            lastMessageStartIndex = lastMessageStartIndex - fragmentSize + charIndex
        else: break

    for message in reversed(messages):
        try:
            if type(messagesClass) == Message:
                await messagesClass.answer(message)
            else:
                await messagesClass.send_message(chat_id=userId, text=message)
        except Exception as e:
            print(e)
            await messagesClass.answer(Strs.get(Strs.ERR_WIKI_LIMIT))
            return
        
    
def assembleMenuText(menuName, userId) -> str:
    formattedSelectedSections = DataManager.get("selectedSections", userId)
    formattedEntriesPerRange = [str(i) for i in DataManager.get("entriesPerRange", userId)]
    holidaysEntries = DataManager.get("holidaysEntries", userId)
    match menuName:
        case "PREF_MAIN":
            return f'''
{Strs.get(Strs.INF_PREFERENCES)}
{Strs.get(Strs.PRF_LANGUAGE)} - <code>{DataManager.get("lang", userId)}</code>
{Strs.get(Strs.PRF_SECTIONS)} - <code>{", ".join(formattedSelectedSections)}</code>
{Strs.get(Strs.PRF_ENTRIES)} - <code>{", ".join(formattedEntriesPerRange) + f", {holidaysEntries}"}</code>
{Strs.get(Strs.PRF_TIME)} - <code>{DataManager.get("scheduledHour", userId)}:00</code>
                    '''
        case "PREF_SECTIONS":
            return f'''
{Strs.get(Strs.INF_SECTIONS)}
{"✔" if formattedSelectedSections.count("Events") > 0 else "❌"} {Strs.get(Strs.PRF_SECTION_EVENTS)}
{"✔" if formattedSelectedSections.count("Births") > 0 else "❌"} {Strs.get(Strs.PRF_SECTION_BIRTHS)}
{"✔" if formattedSelectedSections.count("Deaths") > 0 else "❌"} {Strs.get(Strs.PRF_SECTION_DEATHS)}
{"✔" if formattedSelectedSections.count("Holidays and observances") > 0 else "❌"} {Strs.get(Strs.PRF_SECTION_HOLIDAYS)}
                    ''' 
        case "PREF_ENTRIES":
            return f'''
{Strs.get(Strs.INF_ENTRIES)}
{Strs.get(Strs.PRF_ENTRIES_PRE1600)}: <code>{formattedEntriesPerRange[0]}</code>
{Strs.get(Strs.PRF_ENTRIES_1601_1900)}: <code>{formattedEntriesPerRange[1]}</code>
{Strs.get(Strs.PRF_ENTRIES_MODERN)}: <code>{formattedEntriesPerRange[2]}</code>
{Strs.get(Strs.PRF_ENTRIES_MODERN)}: <code>{holidaysEntries}</code>
                    ''' 
        case "PREF_ENTRIES_INPUT":
            return f'''
{Strs.get(Strs.INF_ENTRIES_INPUT)}
                    ''' 
        case "PREF_TIME_INPUT":
            return f'''
{Strs.get(Strs.INF_TIME_INPUT)}
                    '''
