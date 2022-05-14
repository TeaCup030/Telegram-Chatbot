# Keyboard
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton

# MENU keyboard
KEYBOARD_MENU = [['/Help', '/FAQ', '/QUIZ', '/INFO']]
# QUIZ Keyboard
KEYBOARD_NUMBER = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
# Agreement
KEYBOARD_agreement2 = [["Agree", "Disagree"]]
# Gender
KEYBOARD_Gender = [['M', 'F']]
# Confirm
KEYBOARD_Confirm = [['/Enter_Again', 'Confirm']]
# Ready for Test
KEYBOARD_Ready = [['/NOT_READY', '/READY']]
# for testing
KEYBOARD_NAME = [['TESTING']]
# Continue
KEYBOARD_CONTINUE = [['/Continue']]
# OK
KEYBOARD_OK = [['/OK']]
# result
KEYBOARD_RESULT = [['/Result','/END']]
# for skip question
KEYBOARD_SKIP = [['/skip']]
# for CANCEL
KEYBOARD_CANCEL = [['/cancel']]
# for END
KEYBOARD_END = [['/END']]
# Information MENU
KEYBOARD_INFORMATION_MENU = [['About ADHD', 'About ASD'],
                             ['About Learning Difficulties'],
                             ['Other Support', 'More Information']]

KEYBOARD_FAQ_MENU = [['What kind of test does the chatbot use ?'],
                     ['How long do you keep the data?'],
                     ['What are the Estimated standard scores of cognitive diagnosis tests ?']]

KEYBOARD_RETURN_FAQ = [['/FAQ', '/MENU']]
# Pass / Fail
KEYBOARD_PassFail = [['/Pass', '/Fail']]




# Keyboard Handler
def keyboard_handler(keyboard, one_time, placeholder):
    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=one_time,
                                       resize_keyboard=True,
                                       input_field_placeholder=placeholder)
    return reply_markup


# inline Keyboard
INLINE_KEYBOARD_WEBSITE = [
    [InlineKeyboardButton("Child Assessment Service",
                          callback_data='1', url="https://www.dhcas.gov.hk/en/index.html")
     ],
    [InlineKeyboardButton("ADHD Foundation",
                          callback_data='2', url="http://www.adhd.hk/web/subpage.php?mid=48")],
    [InlineKeyboardButton("Autism Spectrum Disorder",
                          callback_data='3', url="https://www.cdc.gov/ncbddd/autism/index.html")],
]
