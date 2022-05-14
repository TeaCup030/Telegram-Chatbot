from telegram.ext import Updater, ConversationHandler, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
import constants as const
import command_handler as cmd_hdl
import msg_handler as msg_hdl
import logger
import getUserInfo as getUserInfo
import test_handler_v2 as test_hdl


def error(update, context):
    logger.log.error(f"\nUpdate {update} cause error {context.error}\n")


def main():
    updater = Updater(const.API_KEY, use_context=True)
    dp = updater.dispatcher
    # handle get user information
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Agree|agree|/agree)$"), getUserInfo.user_information),
                      MessageHandler(Filters.regex("^(Disagree|disagree|/disagree)$"), getUserInfo.disagree_handle)],
        states={
            getUserInfo.NAME: [
                MessageHandler(Filters.regex('^[A-Za-z\s]+$') & ~Filters.command, getUserInfo.name),
                CommandHandler('cancel', getUserInfo.cancel),
                MessageHandler(Filters.regex('^[\W\d\s^\w]+$') & ~Filters.command, getUserInfo.invalid_name)
            ],
            getUserInfo.GENDER: [
                MessageHandler(Filters.regex('[M|F]') & ~Filters.command, getUserInfo.gender),
                CommandHandler('cancel', getUserInfo.cancel),
                MessageHandler(Filters.regex('^[\W\w\d\s]+$') & ~Filters.command, getUserInfo.invalid_gender)
            ],
            getUserInfo.AGE: [
                MessageHandler(Filters.regex('[\d]+') & ~Filters.command, getUserInfo.age),
                CommandHandler('cancel', getUserInfo.cancel),
                MessageHandler(Filters.regex('[\W\s\w\d]+') & ~Filters.command, getUserInfo.invalid_age)
            ],
            getUserInfo.DOB: [
                MessageHandler(Filters.regex('[\d]{2}-[\d]{2}-[\d]{4}') & ~Filters.command,
                               getUserInfo.dob),
                CommandHandler('cancel', getUserInfo.cancel), #reenter_dob
                MessageHandler(Filters.regex('[\W\sA-Za-z^-]+') & ~Filters.command, getUserInfo.invalid_dob)
            ],
            getUserInfo.CONFIRM: [
                MessageHandler(Filters.regex('^(Confirm)$') & ~Filters.command,
                               getUserInfo.confirm_input),
                CommandHandler('cancel', getUserInfo.cancel),
                CommandHandler('Enter_again', getUserInfo.input_again),
                CommandHandler('confirm', getUserInfo.input_again)
            ],
        },
        fallbacks=[CommandHandler('cancel', getUserInfo.cancel)],
    )

    # handle Test message
    # GUIDELINE, FORWARD_QUESTION, SWITCH, BACKWARD_QUESTION, RESULT
    start_test_handler = ConversationHandler(
        entry_points=[
                      CommandHandler('ready', test_hdl.start_test),
                      CommandHandler('not_ready', test_hdl.not_ready)
                      ],
        states={
            test_hdl.GUIDELINE: [CommandHandler('continue', test_hdl.show_guideline),
                                 CommandHandler('stop', test_hdl.cancel)
                                 ],
            test_hdl.FORWARD_QUESTION: [MessageHandler(Filters.regex('[\d]+'), test_hdl.forward_question),
                                        CommandHandler('OK', test_hdl.forward_question),
                                        CommandHandler('stop', test_hdl.cancel)
                                        ],
            test_hdl.SWITCH: [CommandHandler('continue', test_hdl.switch),
                              CommandHandler('stop', test_hdl.cancel)
                              ],
            test_hdl.BACKWARD_QUESTION: [MessageHandler(Filters.regex('[\d]+'), test_hdl.backward_question),
                                         CommandHandler('continue', test_hdl.backward_question),
                                         CommandHandler('stop', test_hdl.cancel)
                                         ],
            test_hdl.RESULT: [CommandHandler('result', test_hdl.result),
                              CommandHandler('end', test_hdl.test_end)
                              ],
            test_hdl.SUGGESTION: [CommandHandler('pass', test_hdl.result_pass),
                                  CommandHandler('fail', test_hdl.result_fail),
                                  CommandHandler('end', test_hdl.test_end)
                                 ],
            test_hdl.END: [CommandHandler('end', test_hdl.test_end)
                                  ],
            test_hdl.next_forQ: [MessageHandler(Filters.regex('[\d]+'), test_hdl.forward_question),
                                 CommandHandler('stop', test_hdl.cancel)
                                 ],
            test_hdl.next_backQ: [MessageHandler(Filters.regex('[\d]+'), test_hdl.backward_question),
                                  CommandHandler('stop', test_hdl.cancel)
                                  ],
        },
        fallbacks=[CommandHandler('stop', test_hdl.cancel)],
    )

    dp.add_handler(conv_handler)

    dp.add_handler(start_test_handler)

    # List + Loop

    dp.add_handler(CommandHandler("start", cmd_hdl.start_command))

    dp.add_handler(CommandHandler("help", cmd_hdl.help_command))

    dp.add_handler(CommandHandler("menu", cmd_hdl.menu_command))

    dp.add_handler(CommandHandler("quiz", cmd_hdl.quiz_command))

    dp.add_handler(CommandHandler("faq", cmd_hdl.faq_command))

    dp.add_handler(CommandHandler("info", cmd_hdl.info_command))

    dp.add_handler(MessageHandler(Filters.text, msg_hdl.msg_handle))

    # dp.add_handler(CallbackQueryHandler(cmd_hdl.faq_question))

    dp.add_error_handler(error)

    # checking user input // waiting user to input // unit in second
    updater.start_polling(0)
    updater.idle()


# Start the ChatBot
if __name__ == '__main__':
    logger.log.info("Bot started")
    main()
