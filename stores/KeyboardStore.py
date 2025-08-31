from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from . import CallbackStore
import stores.StringStore as Strs


inline, reply = None, None


class Inline:
    def __init__(self, **kwargs):
        for name, markup in kwargs.items():
            setattr(self, name, markup)

class Reply:
   def __init__(self, **kwargs):
        for name, markup in kwargs.items():
            setattr(self, name, markup)


def refreshLocale():
    global inline, reply

    inline = Inline(
        language = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇸/🇬🇧 English", callback_data=CallbackStore.LANGUAGE_ENGLISH)],
            [InlineKeyboardButton(text="🇺🇦 Українська 🤖", callback_data=CallbackStore.LANGUAGE_UKRAINIAN)],
            [InlineKeyboardButton(text="🇪🇸 Español 🤖½", callback_data=CallbackStore.LANGUAGE_SPANISH)],
            [InlineKeyboardButton(text="🇫🇷 Français 🤖½", callback_data=CallbackStore.LANGUAGE_FRENCH)],
            [InlineKeyboardButton(text="🇧🇬 Български 🤖½", callback_data=CallbackStore.LANGUAGE_BULGARIAN)],
        ]),
        tutorial = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_TUTOR_FINISH), callback_data=CallbackStore.TUTORIAL_FINISH)],
        ]),
        restart = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_RESTART_CONTINUE), callback_data=CallbackStore.RESTART_CONTINUE)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_RESTART_CANCEL), callback_data=CallbackStore.RESTART_CANCEL)],
        ]),
        preferences = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=Strs.get(Strs.PRF_LANGUAGE), callback_data=CallbackStore.PREFERENCES_LANGUAGE)],
            [InlineKeyboardButton(text=Strs.get(Strs.PRF_SECTIONS), callback_data=CallbackStore.PREFERENCES_SECTIONS)],
            [InlineKeyboardButton(text=Strs.get(Strs.PRF_ENTRIES), callback_data=CallbackStore.PREFERENCES_ENTRIES)],
            [InlineKeyboardButton(text=Strs.get(Strs.PRF_TIME), callback_data=CallbackStore.PREFERENCES_TIME)],
        ]),
        preferencesSections = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_SECTION_EVENTS), callback_data=CallbackStore.TOGGLE_SECTION_EVENTS)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_SECTION_BIRTHS), callback_data=CallbackStore.TOGGLE_SECTION_BIRTHS)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_SECTION_DEATHS), callback_data=CallbackStore.TOGGLE_SECTION_DEATHS)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_SECTION_HOLIDAYS), callback_data=CallbackStore.TOGGLE_SECTION_HOLIDAYS)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_PREFERENCES_GO_BACK), callback_data=CallbackStore.PREFERENCES_MAIN)],
        ]),
        preferencesEntries = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_ENTRIES_PRE1600), callback_data=CallbackStore.INPUT_ENTRIES_PRE1600)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_ENTRIES_1601_1900), callback_data=CallbackStore.INPUT_ENTRIES_1601_1900)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_ENTRIES_MODERN), callback_data=CallbackStore.INPUT_ENTRIES_MODERN)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_ENTRIES_HOLIDAYS), callback_data=CallbackStore.INPUT_ENTRIES_HOLIDAYS)],
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_PREFERENCES_GO_BACK), callback_data=CallbackStore.PREFERENCES_MAIN)],
        ]),
        preferencesInput = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=Strs.get(Strs.BUT_INPUT_CANCEL), callback_data=CallbackStore.INPUT_CANCEL)],
        ]),
    )
    # reply = Reply(
    #     rndCommand = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
    #         [ButtonStore.reply.askLargerNum]
    #     ]),
    # )   

