from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardRemove, Bot
import keyborad_utils as key_util
import constants as const
import logger
import mongoTestResult

GUIDELINE, FORWARD_QUESTION, SWITCH, BACKWARD_QUESTION, RESULT, SUGGESTION, END = range(7)


def start_test(update: Update, context) -> int:
    logger.log.info("--------------------------START THE TEST --------------------------")
    update.message.reply_text(
        'Now we will start a simple Test. Listen the instruction carefully and answer the question',
        reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_CONTINUE, True, "Continue")
    )
    return GUIDELINE


def not_ready(update: Update, context) -> int:
    logger.log.info("-------------------------- NOT READY --------------------------")
    update.message.reply_text(
        'When You ready, please press /quiz',
        reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_MENU, True, "Return to Menu")
    )
    return ConversationHandler.END


def show_guideline(update: Update, context: CallbackContext) -> int:
    logger.log.info("--------------------------Show Test Guideline --------------------------")
    context.user_data['current_quest'] = 1  # current_quest = current question number
    context.user_data['question_count'] = 0  # current_bd = Current question type
    context.user_data['current_bd'] = 'Forward'
    context.user_data['Forward_correct'] = 0
    context.user_data['Backward_correct'] = 0
    Bot(const.API_KEY).send_audio(chat_id=update.message.chat_id,
                                  audio=open(r'voice/Start.mp3', 'rb'))
    update.message.reply_text(const.INSTRUCTION_FORWARD_1)
    update.message.reply_text(const.INSTRUCTION_FORWARD_2,
                              reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_OK, True, ""))
    return FORWARD_QUESTION


def forward_question(update: Update, context: CallbackContext) -> int:
    logger.log.info("--------------------------Forward Question --------------------------")
    if (context.user_data['current_quest'] > 1):
        update.message.reply_text("Your answer is saved")
        user_answer = str(update.message.text)
        logger.log.info("User Answer: %s", user_answer)
        mongoTestResult.insert_User_answer(update, context, user_answer)

    # if int(context.user_data['current_quest']) == 5:
    if int(context.user_data['current_quest']) == 17: # forward question 1-16
        logger.log.info("----------------END FORWARD PART ---------------")
        update.message.reply_text("Part 1 - Forward Question is End\n "
                                  "Press /continue to move into next part.",
                                  reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_CONTINUE, True, "Continue"))
        return SWITCH  # call result
    else:
        update.message.reply_text(const.for_questions_string[context.user_data['current_quest'] - 1])
        if context.user_data['current_bd'] == 'Forward':
            Bot(const.API_KEY).send_audio(chat_id=update.message.chat_id,
                                          audio=open(
                                              r'voice/Forward/' + str(context.user_data['current_quest']) + '.mp3',
                                              'rb'))
        else:
            update.message.reply_text("Your answer is ....?")
        context.user_data['current_quest'] += 1
        context.user_data['question_count'] += 1
        logger.log.info('current_quest : %s', context.user_data['current_quest'])
        logger.log.info('question_count : %s', context.user_data['question_count'])
        return next_forQ


def next_forQ(update: Update, context: CallbackContext) -> int:
    return FORWARD_QUESTION


def switch(update: Update, context: CallbackContext) -> int:
    logger.log.info("--------------------------SWITCH --------------------------")
    context.user_data['current_quest'] = 1
    context.user_data['current_bd'] = 'Backward'
    Bot(const.API_KEY).send_audio(chat_id=update.message.chat_id,
                                  audio=open(r'voice/Backward.mp3', 'rb'))
    update.message.reply_text("Now I am going to say some more numbers but this time when I stop I want you to say "
                              "them backwards.")
    update.message.reply_text("For example, if I say 9 2 7, you should say 729.")
    update.message.reply_text("Please press /continue to start part 2 - Backward question",
                              reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_CONTINUE, True, "Continue"))
    logger.log.info("--------------------------MOVE TO BACKWARD PART --------------------------")
    return BACKWARD_QUESTION


def backward_question(update: Update, context: CallbackContext) -> int:
    if (context.user_data['current_quest'] > 1):
        update.message.reply_text("Your answer is saved")
        # TODO: store in MonogoDB + check the answer
        user_answer = str(update.message.text)
        logger.log.info("User Answer: %s", user_answer)
        mongoTestResult.insert_User_answer(update, context, user_answer)

    # if int(context.user_data['current_quest']) == 5:  # total backward = 14
    if int(context.user_data['current_quest']) == 15:  # total backward = 14
        update.message.reply_text("All question done",
                                  reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_RESULT, True, "Result"))
        return RESULT  # call result
    else:
        update.message.reply_text(const.back_questions_string[context.user_data['current_quest'] - 1])
        if context.user_data['current_bd'] == 'Backward' and int(context.user_data['current_quest']) <= 14:
            Bot(const.API_KEY).send_audio(chat_id=update.message.chat_id,
                                          audio=open(
                                              r'voice/Backward/' + str(context.user_data['current_quest']) + '.mp3',
                                              'rb'))
        else:
            update.message.reply_text("Your answer is ....?")
        context.user_data['current_quest'] += 1
        context.user_data['question_count'] += 1
        logger.log.info('current_quest : %s', context.user_data['current_quest'])
        logger.log.info('question_count : %s', context.user_data['question_count'])
        return next_backQ


def next_backQ(update: Update, context: CallbackContext) -> int:
    return backward_question


def result(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    logger.log.info("-------------------------- Result Part  --------------------------")
    user = update.message.from_user
    logger.log.info("END of %s: %s", user.first_name, update.message.text)
    mongoTestResult.insert_total(update, context)
    logger.log.info("-------------------------- END result --------------------------")
    result_auto(update, context)
    return SUGGESTION


def result_auto(update: Update, context: CallbackContext) -> int:
    logger.log.info("-------------------------- Showsuggestion  --------------------------")
    logger.log.info(context.user_data['userResult'])
    if context.user_data['userResult'] is True:
        logger.log.info("-------------------------- Pass  --------------------------")
        update.message.reply_text(
            'Your result is great.'
            , reply_markup=ReplyKeyboardRemove()
        )
        Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                        'CAACAgUAAxkBAAIn12JQGWl7Rh5TsYYes8aA6GUT5dc_AAK3GwACuJsaFoZtIUWYRB7rIwQ')
        update.message.reply_text('Press /END to end or exit the quiz ',
                                  reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_END, True, "\END"))
    elif context.user_data['userResult'] is False:
        # Fail case
        logger.log.info("-------------------------- Fail  --------------------------")
        update.message.reply_text(
            'Here are some Suggestion / guideline for you :\n 1. \n 2.\n 3.\n'
            ,reply_markup=ReplyKeyboardRemove()
        )
        Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                        'CAACAgUAAxkBAAIn2WJQGZadiGI91kZ89IF-AAGwy9r8JgACuBYAAp7UXgNmpFskDIVLziME')
        Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                        'CAACAgIAAxkBAAIn2GJQGYaY6hXzH8cDUhIVkmZEkC_FAAI7LgAC4KOCB8isTcEjMO7JIwQ')
        update.message.reply_text('Press /END to end/exit the quiz ',
                                  reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_END, True, "\END"))
    logger.log.info("-------------------------- END --------------------------")
    return END


def result_pass(update: Update, context: CallbackContext) -> int:
    logger.log.info("-------------------------- Pass  --------------------------")
    update.message.reply_text(
        'Your result is great.'
        , reply_markup=ReplyKeyboardRemove()
    )
    logger.log.info("-------------------------- END --------------------------")
    return END


def result_fail(update: Update, context: CallbackContext) -> int:
    logger.log.info("-------------------------- Fail  --------------------------")
    update.message.reply_text(
        'Here are some Suggestion / guideline for you :\n 1. \n 2.\n 3.\n'
        , reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text('Press /END to end/exit the quiz ',
                              reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_END, True, "\END"))
    logger.log.info("-------------------------- END --------------------------")
    return END


def test_end(update: Update, context: CallbackContext) -> int:
    logger.log.info("-------------------------- END  --------------------------")
    Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                    'CAACAgIAAxkBAAIngGJQFiCYLWnvS9zN1s6mUb5p60kZAAJvEgAC6NbiEqzaRJ6rzOTOIwQ')
    update.message.reply_text(
        'This the end of the test. Bye ~', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.log.info("User %s canceled the conversation.", user.first_name)
    Bot(const.API_KEY).send_sticker(update.message.chat_id,
                                    'CAACAgIAAxkBAAIngGJQFiCYLWnvS9zN1s6mUb5p60kZAAJvEgAC6NbiEqzaRJ6rzOTOIwQ')
    update.message.reply_text(
        'Bye! This is the end of the test. \nIf you want test again, press /quiz.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
