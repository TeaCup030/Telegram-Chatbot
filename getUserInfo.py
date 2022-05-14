from telegram.ext import ConversationHandler, CallbackContext
from telegram import ReplyKeyboardRemove, Update, Bot
from datetime import date, datetime
import constants as const
import logger
import keyborad_utils as key_util
import mongoGetJSON

NAME, GENDER, AGE, DOB, CONFIRM = range(5)


def user_information(update: Update, context: CallbackContext):
    update.message.reply_text(const.Cancel_getInfo)
    update.message.reply_text(
        'Enter Your Name', reply_markup=ReplyKeyboardRemove(),
    )
    logger.log.info("---------------CALL Insert Data----------------")
    # getJSON.new_user(update, context)
    mongoGetJSON.new_user_mongo(update, context)
    return NAME


def name(update: Update, context: CallbackContext)->int:
    # user = update.message.from_user
    logger.log.info("Name of %s: %s", update.message.chat.first_name, update.message.text)
    user_msg = str(update.message.text)
    mongoGetJSON.update_UserInfo(update, context, "name", user_msg)
    # intoDB.update_user_information(update, context, "name", user_msg)
    update.message.reply_text(
        'Enter the gender',
        reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_Gender, True, "M / F"),
    )
    return GENDER


def gender(update, context: CallbackContext) -> int:
    logger.log.info("Gender of %s: %s", update.message.chat.first_name, update.message.text)
    user_msg = str(update.message.text)
    mongoGetJSON.update_UserInfo(update, context, "sex", user_msg)
    # intoDB.update_user_information(update, context, "sex", user_msg)
    update.message.reply_text(
        'Enter your age:',
        reply_markup=ReplyKeyboardRemove(),
    )
    return AGE


def age(update, context: CallbackContext) -> int:
    logger.log.info("Age of %s: %s", update.message.chat.first_name, update.message.text)
    user_msg = str(update.message.text)
    check_age(update, context, user_msg)
    if context.user_data['age_check'] is True:
        mongoGetJSON.update_UserInfo(update, context, "age", user_msg)
        context.user_data['age'] = int(user_msg)
        logger.log.debug('--------------------END-AGE---------------------')
        update.message.reply_text(
            'Enter Date of Birth DD-MM-YYYY:',
            reply_markup=ReplyKeyboardRemove(),
        )
        return DOB
    else:
        logger.log.info('--------------------Enter again---------------------')
        return AGE


def dob(update, context: CallbackContext) -> int:
    user_msg = str(update.message.text)
    # check validation
    context.user_data['dob_check'] = False
    check_dob(update, context, user_msg)
    if context.user_data['dob_check'] is True:
        # intoDB.update_user_information(update, context, "dob", user_msg)
        # dbUpdateUserInfo.show_user_info(update, context)
        mongoGetJSON.update_UserInfo(update, context, "dob", user_msg)
        mongoGetJSON.confirm_info(update, context)
        logger.log.debug('--------------------END update record ---------------------')
        logger.log.info('--------------------END-DOB---------------------')
        return CONFIRM
    else:
        logger.log.info('--------------------Enter again---------------------')
        return DOB


def confirm_input(update, context: CallbackContext) -> int:
    logger.log.debug('-----------------END---------------------')
    logger.log.info("Confirm the information %s :%s", update.message.chat.first_name, update.message.text)
    update.message.reply_text(
        const.Check_ready,
        reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_Ready, True, "READY"),
    )
    return ConversationHandler.END


def input_again(update, context: CallbackContext) -> int:
    logger.log.debug('----------------- INPUT AGAIN --------------------')
    update.message.reply_text(
        'Enter Your Name', reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


def disagree_handle(update: Update, context: CallbackContext) -> int:
    logger.log.info("User %s canceled the conversation.", update.message.chat.first_name)
    update.message.reply_text(
        "You Must agree the statement before starting the quiz\n"
        "Please return to /quiz",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def cancel(update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    # user = update.message.from_user
    logger.log.info("User %s canceled the Get User Information Step.", update.message.chat.first_name)
    Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                    'CAACAgIAAxkBAAIngGJQFiCYLWnvS9zN1s6mUb5p60kZAAJvEgAC6NbiEqzaRJ6rzOTOIwQ')
    update.message.reply_text(const.restart_quiz, reply_markup=ReplyKeyboardRemove())
    getJSON.new_user(update, context)
    return ConversationHandler.END


def check_age(update, context, user_message) -> int:
    logger.log.debug('-----------------CHECKING AGE---------------------')
    user_msg = int(update.message.text)
    if 5 < user_msg < 100:
        logger.log.debug("User %s input VALID: %d ", update.message.chat.first_name, user_msg)
        context.user_data['age_check'] = True
        logger.log.debug('-----------------CHECKING END---------------------')
    else:
        logger.log.debug("User %s input INVALID: %d ", update.message.chat.first_name, user_msg)
        context.user_data['age_check'] = False
        update.message.reply_text(
            const.incorrect_Age, reply_markup=ReplyKeyboardRemove()
        )
        logger.log.debug('-----------------CHECKING END---------------------')


def check_dob(update, context, user_message) -> int:
    logger.log.debug('-----------------CHECKING DOB---------------------')
    user_msg = str(update.message.text)
    day, month, year = user_message.split('-')
    # isValidDate = True
    try:
        date(int(year), int(month), int(day))
    except ValueError:
        # isValidDate = False
        logger.log.debug("User %s input INVALID: %s ", update.message.chat.first_name, user_message)
        update.message.reply_text(
            const.incorrect_dob, reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['dob_check'] = False

    age = int(datetime.now().year) - int(year)
    logger.log.debug("User %s input: %d ", update.message.chat.first_name, age)
    if date(int(year), int(month), int(day)) >= date.today():
        update.message.reply_text(
            const.incorrect_dob_2, reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['dob_check'] = False
    elif age > 100 :
        logger.log.debug("User %s input INVALID: %d ", update.message.chat.first_name, age)
        update.message.reply_text(const.incorrect_dob_3, reply_markup=ReplyKeyboardRemove())
        context.user_data['dob_check'] = False
    elif age < 6:
        logger.log.debug("User %s input INVALID: %d ", update.message.chat.first_name, age)
        update.message.reply_text(const.incorrect_dob_4, reply_markup=ReplyKeyboardRemove())
        context.user_data['dob_check'] = False
    elif age != int(context.user_data['age']):
        logger.log.debug("User %s input INVALID: %d, %d  ", update.message.chat.first_name, age ,int(context.user_data['age']))
        update.message.reply_text(const.incorrect_dob_5, reply_markup=ReplyKeyboardRemove())
        context.user_data['dob_check'] = False
    else:
        logger.log.debug("User %s input valid: %s ", update.message.chat.first_name, user_message)
        logger.log.info("DOB of %s: %s", update.message.chat.first_name, update.message.text)
        logger.log.debug('-----------------END CHECKING---------------------')
        context.user_data['dob_check'] = True


def invalid_dob(update, context: CallbackContext) -> int:
    logger.log.debug('-----------------INVALID INPUT---------------------')
    logger.log.debug("User %s input INVALID: %s ", update.message.chat.username, update.message.text)
    update.message.reply_text(
        const.incorrect_dob, reply_markup=ReplyKeyboardRemove()
    )
    return DOB


def invalid_gender(update, context: CallbackContext) -> int:
    logger.log.debug('-----------------INVALID INPUT---------------------')
    logger.log.debug("User %s input INVALID: %s ", update.message.chat.username, update.message.text)
    update.message.reply_text(
        const.incorrect_gender, reply_markup=ReplyKeyboardRemove()
    )
    return GENDER


def invalid_name(update, context: CallbackContext) -> int:
    logger.log.debug('-----------------INVALID INPUT---------------------')
    logger.log.debug("User %s input INVALID: %s ", update.message.chat.username, update.message.text)
    update.message.reply_text(
        const.incorrect_Name, reply_markup=ReplyKeyboardRemove()
    )
    return NAME


def invalid_age(update, context: CallbackContext) -> int:
    logger.log.debug('-----------------INVALID INPUT---------------------')
    logger.log.debug("User %s input INVALID: %s ", update.message.chat.username, update.message.text)
    update.message.reply_text(
        const.incorrect_Age, reply_markup=ReplyKeyboardRemove()
    )
    return AGE
