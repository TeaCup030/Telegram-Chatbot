from telegram import InlineKeyboardMarkup,Bot
import constants as const
import keyborad_utils as key_utl
from conversation import chatbot_response


def msg_handle(update, context):

    user_message = str(update.message.text)

    if user_message == 'Author':
        update.message.reply_text(const.Who_Create)
        update.message.reply_text(const.RETURN_INFO_MENU)

    elif user_message == 'About ADHD':
        update.message.reply_text(const.ADHD_INFO_01)
        update.message.reply_text(const.RETURN_INFO_MENU)

    elif user_message == 'About ASD':
        update.message.reply_text(const.ASD_INFO_01)
        update.message.reply_text(const.ASD_INFO_02)
        update.message.reply_text(const.RETURN_INFO_MENU)

    elif user_message == 'About Learning Difficulties':
        update.message.reply_text(const.LD_INFO_01)
        update.message.reply_text(const.RETURN_INFO_MENU)

    elif user_message == 'Other Support':
        update.message.reply_text("I'm working on it. Please wait.....")
        Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                        'CAACAgIAAxkBAAInaWJQFXpMUH4gRV6aTuFvJE-lGI_RAAJsAQACFkJrCv34eDXnr5jgIwQ')
        update.message.reply_text(const.RETURN_INFO_MENU)

    elif user_message == 'More Information':
        update.message.reply_text(const.MI_INFO_01)
        update.message.reply_text(const.MI_INFO_02,
                                  reply_markup=InlineKeyboardMarkup(key_utl.INLINE_KEYBOARD_WEBSITE))

    elif user_message == 'What kind of test does the chatbot use ?':
        update.message.reply_text("It uses digit span test.It is a very short test that evaluates a person's cognitive "
                                  "status. It is frequently used in hospitals and physicians' offices in order for a "
                                  "clinician to quickly evaluate whether a patient's cognitive abilities are normal "
                                  "or impaired.",
                                  reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_RETURN_FAQ, True, ""))

    elif user_message == 'How long do you keep the data?':
        update.message.reply_text("THe user data will keep 3 months.",
                                  reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_RETURN_FAQ, True, ""))

    elif user_message == 'What are the Estimated standard scores of cognitive diagnosis tests ?':
        update.message.reply_text("Here is the reference document",
                                  reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_RETURN_FAQ, True, ""))
        Bot(const.API_KEY).send_document(update.message.chat_id,
                                         document=open('doc/Auditory_Memory_Digit_Test.pdf', 'rb'),
                                         filename="Reference.pdf")
    elif user_message == 'What is your test result ?':
        update.message.reply_text("I'm a robot, I cannot do the test.",
                                  reply_markup=key_utl.keyboard_handler(key_utl.KEYBOARD_RETURN_FAQ, True, ""))

    elif user_message != '':
        msg = user_message.lower()
        res = chatbot_response(msg)
        update.message.reply_text(res)

    else:
        update.message.reply_text("Sorry, I don't understand")
