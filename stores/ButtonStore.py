from aiogram.utils.keyboard import KeyboardButton, InlineKeyboardButton

from . import CallbackStore
import stores.StringStore as Strs

inline, reply = None, None


class Inline:
    def __init__(self, **kwargs):
        for name, button in kwargs.items():
            setattr(self, name, button)

class Reply:
    def __init__(self, **kwargs):
        for name, button in kwargs.items():
            setattr(self, name, button)


def refreshLocale():
    global inline, reply
    inline = Inline(
        echoUpper = InlineKeyboardButton(text=Strs.get(Strs.BUT_ECHO_UPPER), callback_data=CallbackStore.ECHO_UPPER),
        echoCapitalize = InlineKeyboardButton(text=Strs.get(Strs.BUT_ECHO_CAPITALIZE), callback_data=CallbackStore.ECHO_CAPITALIZE),

        tutorialFinish = InlineKeyboardButton(text=Strs.get(Strs.BUT_TUTOR_FINISH), callback_data=CallbackStore.TUTORIAL_FINISH),

        languageEnglish = InlineKeyboardButton(text="🇺🇸/🇬🇧 English", callback_data=CallbackStore.LANGUAGE_ENGLISH),
        languageRouter = InlineKeyboardButton(text="📻 router", callback_data=CallbackStore.LANGUAGE_ROUTER),

        restartContinue = InlineKeyboardButton(text=Strs.get(Strs.BUT_RESTART_CONTINUE), callback_data=CallbackStore.RESTART_CONTINUE),
        restartCancel = InlineKeyboardButton(text=Strs.get(Strs.BUT_RESTART_CANCEL), callback_data=CallbackStore.RESTART_CANCEL),

        preferencesLanguage = InlineKeyboardButton(text=Strs.get(Strs.PRF_LANGUAGE), callback_data=CallbackStore.PREFERENCES_LANGUAGE),
    )
    reply = Reply(
        askLargerNum = KeyboardButton(text="I need larger number!"),
    )
