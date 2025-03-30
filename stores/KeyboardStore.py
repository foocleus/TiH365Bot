from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup

from . import ButtonStore

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

    ButtonStore.refreshLocale()
    inline = Inline(
        echo = InlineKeyboardMarkup(inline_keyboard=[
            [ButtonStore.inline.echoUpper],
            [ButtonStore.inline.echoCapitalize]
        ]),
        language = InlineKeyboardMarkup(inline_keyboard=[
            [ButtonStore.inline.languageEnglish],
            [ButtonStore.inline.languageRouter],
        ]),
        tutorial = InlineKeyboardMarkup(inline_keyboard=[
            [ButtonStore.inline.tutorialFinish],
        ]),
        restart = InlineKeyboardMarkup(inline_keyboard=[
            [ButtonStore.inline.restartContinue],
            [ButtonStore.inline.restartCancel],
        ]),
        preferences = InlineKeyboardMarkup(inline_keyboard=[
            [ButtonStore.inline.preferencesLanguage],
        ]),
    )
    reply = Reply(
        rndCommand = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
            [ButtonStore.reply.askLargerNum]
        ]),
    )   

