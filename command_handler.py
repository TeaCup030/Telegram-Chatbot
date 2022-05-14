from telegram import Bot, Update
from telegram.ext import CallbackContext
import logger
import constants as const
import keyborad_utils as key_utl


def start_command(update, context):
    logger.log.debug('----------------START COMMAND---------------------')
    greeting_msg = "Hi," + str(update.message.chat.first_name)
    update.message.reply_text(greeting_msg)
    Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                    'CAACAgIAAxkBAAInZGJQFSqnDsoUV5gZWBxTkCrK2AmQAAJnAQACFkJrCnOJvs6llmgiIwQ')
    update.message.reply_text(const.Greeting_hau,
                              reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_MENU, True, ""))


def help_command(update, context):
    logger.log.debug('-----------------HELP COMMAND---------------------')
    update.message.reply_text(const.Help_statement,
                              reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_MENU, True, ""))


def menu_command(update, context):
    logger.log.debug('-----------------MENU COMMAND---------------------')
    update.message.reply_text(const.Menu_statement,
                              reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_MENU, True, ""))


def quiz_command(update, context):
    logger.log.debug('-----------------QUIZ COMMAND---------------------')
    update.message.reply_text(const.Agreement_statement,
                              reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_agreement2, True, ""))


def faq_command(update, context):
    logger.log.debug('-----------------FAQ COMMAND---------------------')
    update.message.reply_text(const.FAQ_statement,
                              reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_FAQ_MENU, True, ""))


def info_command(update, context):
    logger.log.debug('-----------------Information COMMAND---------------------')
    update.message.reply_text(const.Info_statement,
                              reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_INFORMATION_MENU, True, ""))


def faq_question(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    # query.answer()
    if str(query.data) == '1':
        Bot(const.API_KEY).send_message(chat_id=update.message.chat_id,
                                        text="It is a Digit Span Test that is a cognitive diagnosis test.")
        # query.edit_message_text(text="It is a Digit Span Test that is a cognitive diagnosis test.")
    elif str(query.data) == '2':
        query.edit_message_text("All the data will be automatically deleted after 3 months")
    else:
        query.edit_message_text("N.A")
