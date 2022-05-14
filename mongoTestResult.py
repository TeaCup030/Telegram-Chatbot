from datetime import datetime
import pymongo
import logger
import keyborad_utils as key_util


def insert_User_answer(update, context, qAns):
    try:
        # connect monogoDb client
        # db = pymongo.MongoClient('', username='', password='')
        # Cloud
        # db = pymongo.MongoClient('')
        logger.log.info('----------------Connect database Mongodb -------------')
        col = db['fyp']
        logger.log.info('---------------- Database fyp -------------')
        chat_id = update.message.chat_id
        current_timestamp = datetime.now()
        qusetNum = int(context.user_data['question_count'])
        logger.log.info('qusetNum: %s', qusetNum)
        user_ans = int(update.message.text)
        logger.log.info('user_ans: %s', user_ans)
        qAnswer = col['questionNanswer'].find_one({'QNum': qusetNum}, {'_id': 0, 'Answer': 1})
        logger.log.info('---------------- FIND ONE -------------')
        if int(user_ans) == int(qAnswer['Answer']):
            insert_answer = {'User_Id': chat_id,
                             'updateTmp': current_timestamp,
                             'question_Num': qusetNum,
                             'user_ans': user_ans,
                             'check': 'True'}
            logger.log.info('%s Answer is Correct (%s,%s)', qusetNum, user_ans, qAnswer['Answer'])
            if 0 < int(qusetNum) < 17:
                context.user_data['Forward_correct'] += 1
                logger.log.info('Forward Total : %s ', context.user_data['Forward_correct'])
            elif 16 < int(qusetNum) < 31:
                context.user_data['Backward_correct'] += 1
                logger.log.info('Backward Total : %s ', context.user_data['Backward_correct'])
            col.userAnswer.insert_one(insert_answer)
            logger.log.info('---------------- Mongodb insert User answer :%s ,%s-------------', qusetNum, user_ans)
        else:
            insert_answer = {'User_Id': chat_id,
                             'updateTmp': current_timestamp,
                             'question_Num': qusetNum,
                             'user_ans': user_ans,
                             'check': 'False'}
            logger.log.info('%s Answer is Wrong (%s,%s)', qusetNum, user_ans, qAnswer['Answer'])
            col.userAnswer.insert_one(insert_answer)
            logger.log.info('---------------- Mongodb insert User answer :%s ,%s-------------', qusetNum, user_ans)
    except Exception as e:
        logger.log.error(e)


def insert_total(update, context):
    try:
        # connect monogoDb client
        # db = pymongo.MongoClient('', username='', password='')
        # Cloud
        # db = pymongo.MongoClient('')
        logger.log.info('----------------Connect database Mongodb -------------')
        db = db['fyp']
        logger.log.info('---------------- Database fyp -------------')
        logger.log.info("-------------------------- Insert total score--------------------------")
        chat_id = update.message.chat_id
        current_timestamp = datetime.now()
        forward_total = int(context.user_data['Forward_correct'])
        backward_total = int(context.user_data['Backward_correct'])
        total_score = int(forward_total) + int(backward_total)
        logger.log.info('%d',total_score)
        check_result(update, context, total_score)
        std_score = str(context.user_data['StdScore'])
        logger.log.info('---------------- std_score -------------')
        equivalent = str(context.user_data['PercentileEquivalent'])
        logger.log.info('---------------- Mongodb insert -------------')
        insertResult = {
            'User_Id': chat_id,
            'Total_forward_score': forward_total,
            'Total_backward_score': backward_total,
            'Total_score': total_score,
            'Standard_score': std_score,
            'Percentile_equivalent': equivalent,
            'updateTmp': current_timestamp
        }
        db.userResult.insert_one(insertResult)
        logger.log.info("-------------------------- Print the result --------------------------")
        update.message.reply_text(
            "Here is the test result: \nTotal Forwards score :" +str(forward_total)+
            "\nTotal Backward score :" +str(backward_total)+
            "\nTotal Score:" +str(total_score)+
            "\nStandard score:"+str(std_score)+
            "\nPercentile equivalent:"+str(equivalent)
        )
        logger.log.info("-------------------------- Check Pass Fail --------------------------")
        if float(equivalent) > 50:
            update.message.reply_text("Your Result : Pass \n "
                                      "Your score is higher than the average",
                                      reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_PassFail, True, ""))
            context.user_data['userResult'] = True
        elif float(equivalent) < 50:
            update.message.reply_text("Your Result : Fail \n "
                                      "Your score is below the average",
                                      reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_PassFail, True, ""))
            context.user_data['userResult'] = False
    except Exception as e:
        logger.log.error(e)
    logger.log.info(context.user_data['userResult'])


def check_result(update, context, rawScore):
    try:
        # connect monogoDb client
        # db = pymongo.MongoClient('', username='', password='')
        # Cloud
        # db = pymongo.MongoClient('')
        logger.log.info('----------------Connect database Mongodb -------------')
        col = db['fyp']
        chat_id = update.message.chat_id
        logger.log.info("-------------------------- Check Standard score --------------------------")
        findAge = col['chatbotuser'].find_one({'User_Id': chat_id}, {'_id': 0, 'Age': 1}, sort=[('updateTmp', -1)])
        userAge = str(findAge['Age'])
        if int(userAge) > 18:
            userAge = '18'
        logger.log.info('User Age %s', userAge)
        totalScore = str(rawScore)
        findStd = col['score2StdScoreV2'].find_one({'Score': totalScore}, {'_id': 0, userAge: 1})
        StdScore = str(findStd[userAge])
        logger.log.info('Standard Score: %s', StdScore)
        context.user_data['StdScore'] = StdScore
        # out of the table record
        if int(StdScore) > 145:
            StdScore = '145'
        if int(StdScore) < 54:
            StdScore = '54'
        # check out of change
        if StdScore is None:
            context.user_data['StdScore'] = 'out of range'
            context.user_data['PercentileEquivalent'] = 'Out of Range'
            logger.log.info("-------------------------- BREAK --------------------------")
            return True
        logger.log.info("-------------------------- Percentile Equivalent --------------------------")
        # Percentile Equivalent
        findpent = col['stdScore2equiv'].find_one({'StandardScore': StdScore}, {'_id': 0, 'PercentileEquivalent ': 1})
        context.user_data['PercentileEquivalent'] = str(findpent['PercentileEquivalent '])
        logger.log.info('Percentile Equivalent: %s', str(findpent['PercentileEquivalent ']))
        if context.user_data['PercentileEquivalent'] is None:
            context.user_data['PercentileEquivalent'] = 'Out of Range'
        logger.log.info('Percentile Equivalent -2: %s',context.user_data['PercentileEquivalent'])
    except Exception as e:
        logger.log.error(e)
