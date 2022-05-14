from datetime import datetime
import pymongo
import logger
from telegram.ext import *
import keyborad_utils as key_util



def new_user_mongo(update, context: CallbackContext):
    try:
        # connect monogoDb client
        # db = pymongo.MongoClient('', username='', password='')
        # Cloud
        # db = pymongo.MongoClient('')
        db = db['fyp']
        # connect to database
        logger.log.info('---------------- Database fyp -------------')
        logger.log.info('----------------Connect database Mongodb -------------')
        # get info
        chat_id = update.message.chat_id
        first_name = update.message.chat.first_name
        username = update.message.chat.username
        current_timestamp = datetime.now()
        if update.message.chat.last_name is None:
            last_name = ""
        else:
            last_name = update.message.chat.last_name

        findUserId = {"User_Id": chat_id}
        mydoc = db.chatbotuser.find(findUserId)
        # Insert new record if their chat_id doesn't exist in db.
        logger.log.info('---------------- Mongodb insert -------------')
        insertUserInfo = {
            'User_Id': chat_id,
            'T_FName': first_name,
            'T_LName': last_name,
            'TName': username,
            'Agreement': '',
            'updateTmp': current_timestamp
        }
        db.chatbotuser.insert_one(insertUserInfo)

    except Exception as e:
        logger.log.error('Connect Mongo database is failed')
        logger.log.error(e)


def update_UserInfo(update, context, stts, user_msg):
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

        findRecord = col['chatbotuser'].find_one({"User_Id": chat_id}, sort=[('updateTmp', -1)])
        logger.log.info('---------------- Find user id -------------')
        if stts == 'name':
            col['chatbotuser'].find_one_and_update(findRecord,
                                                   {'$set': {'updateTmp': current_timestamp,
                                                             'Name': user_msg ,
                                                             'Agreement': 'Agree'}})
            logger.log.info('---------------- Mongodb Update User Name :%s-------------', user_msg)
        elif stts == 'sex':
            col['chatbotuser'].find_one_and_update(findRecord,
                                                   {'$set': {'updateTmp': current_timestamp, 'Sex': user_msg}})
            logger.log.info('---------------- Mongodb Update User Sex :%s-------------', user_msg)
        elif stts == 'age':
            col['chatbotuser'].find_one_and_update(findRecord,
                                                   {'$set': {'updateTmp': current_timestamp, 'Age': user_msg}})
            logger.log.info('---------------- Mongodb Update User Age :%s-------------', user_msg)
        elif stts == 'dob':
            col['chatbotuser'].find_one_and_update(findRecord,
                                                   {'$set': {'updateTmp': current_timestamp, 'Dob': user_msg}})
            logger.log.info('---------------- Mongodb Update User Dob :%s-------------', user_msg)

    except Exception as e:
        logger.log.error('Connect Mongo database is failed')
        logger.log.error(e)


def confirm_info(update, context: CallbackContext):
    chat_id = update.message.chat_id
    logger.log.info('Print User %s information', chat_id)
    try:
        # connect monogoDb client
        # db = pymongo.MongoClient('', username='', password='')
        # Cloud
        # db = pymongo.MongoClient('')
        logger.log.info('----------------Connect database Mongodb -------------')
        db = db['fyp']  # collection
        logger.log.info('---------------- Database fyp -------------')
        chat_id = update.message.chat_id
        logger.log.info('---------------- Find user id -------------')
        # chatbotuser = document
        getInfo = db.chatbotuser.find_one({"User_Id": chat_id}, {'_id': 0, 'Name': 1, 'Sex': 1, 'Age': 1, 'Dob': 1},
                                          sort=[('updateTmp', -1)])
        Name = getInfo['Name']
        Sex = getInfo['Sex']
        Age = getInfo['Age']
        dob = getInfo['Dob']
        # --- 1 for asc and -1 for desc
        update.message.reply_text(
            'Please confirm the information : \n'
            'NAME : ' + str(Name) +
            ' \nGENDER : ' + str(Sex) +
            ' \nAGE : ' + str(Age) +
            ' \nDate of Birth : ' + str(dob),
            reply_markup=key_util.keyboard_handler(key_util.KEYBOARD_Confirm, True, ""),
        )
    except Exception as e:
        # Handle Error
        logger.log.error(e)
