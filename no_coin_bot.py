from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import sqlite3
import datetime

import config
import inline_markups
import reply_markups





#  LIBRARY VARIABLES

storage = MemoryStorage()

bot = Bot(config.token)
dp = Dispatcher(bot, storage = MemoryStorage())

db = sqlite3.connect('database.db', check_same_thread = False)
sql = db.cursor()

date_time = datetime.datetime.now().date()



#  STATES

class States(StatesGroup):
    value = State()



#  CREATING DATABASE
sql.execute('CREATE TABLE IF NOT EXISTS user_access (id INTEGER, username TEXT, firstname TEXT, lastname TEXT, date DATE)')
sql.execute('CREATE TABLE IF NOT EXISTS user_data (id INTEGER, balance INTEGER)')
db.commit()





#  START COMMAND

@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    sql.execute('SELECT id FROM user_access WHERE id = ?', (message.chat.id,))
    user_id = sql.fetchone()

    if user_id == None:
        sql.execute('INSERT INTO user_access (id, username, firstname, lastname, date) VALUES (?, ?, ?, ?, ?)',
        (message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, date_time))
        sql.execute('INSERT INTO user_data (id, balance) VALUES (?, ?)',
        (message.chat.id, 0))
        db.commit()

        await bot.send_message(message.chat.id, '<b> Welcome ! </b>', parse_mode = 'html', reply_markup = reply_markups.menu)

    else:
        await bot.send_message(message.chat.id, '<b> Main menu: </b>', parse_mode = 'html', reply_markup = reply_markups.menu)





#  TEXT

@dp.message_handler()
async def text(message: types.Message):
    
    if message.text == '🌕  Майнить':
        sql.execute('SELECT balance FROM user_data WHERE id = ?', (message.chat.id,))
        user_balance = sql.fetchone()[0]
        await bot.send_message(message.chat.id, f'<b> 🌕  Ваш баланс:  {user_balance} </b>', parse_mode = 'html', reply_markup = inline_markups.mine)

    elif message.text == '💰  Баланс':
        sql.execute('SELECT balance FROM user_data WHERE id = ?', (message.chat.id,))
        user_balance = sql.fetchone()[0]
        await bot.send_message(message.chat.id, f'<b> 🌕  Ваш баланс:  {user_balance} </b>', parse_mode = 'html')

    elif message.text == '🏆  Лига':
        await bot.send_message(message.chat.id, f'<b> В разработке . . . </b>', parse_mode = 'html')



    else:
        await bot.send_message(message.chat.id, '<b> TEXT </b>', parse_mode = 'html', reply_markup = None)





#  CALLBACK
@dp.callback_query_handler(lambda call: True)
async def callback_queries(call: types.CallbackQuery):


#  SEND MESSAGE
    if call.data == 'callback_1':
        await bot.send_message(
            chat_id =call.message.chat.id, 
            text = '<b> TEXT </b>', 
            parse_mode = 'html', 
            reply_markup = None)




#  EDIT INLINE TEXT
    elif call.data == 'mine':

        sql.execute('UPDATE user_data SET balance = balance + 1 WHERE id = ?', (call.message.chat.id,))
        db.commit()
        
        sql.execute('SELECT balance FROM user_data WHERE id = ?', (call.message.chat.id,))
        user_balance = sql.fetchone()[0]
        
        await bot.edit_message_text(
            chat_id = call.message.chat.id, 
            message_id = call.message.message_id, 
            text = f'<b> 🌕  Ваш баланс:  {user_balance} </b>', 
            parse_mode = 'html', 
            reply_markup = inline_markups.mine)




#  EDIT INLINE PHOTO
    if call.data == 'edit_photo':
        with open('photo/photo.jpg', 'rb') as photo:
            bot.edit_message_media( 
                media = types.InputMedia(
                type = 'photo',
                media = photo,
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                caption = '<b> TEXT </b>',
                parse_mode = 'html'),
                reply_markup = None)




#  STATES
@dp.message_handler(state = States.value)
async def check_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text

        #  FINISH STATE
        if message.text == 'value':
            await state.finish()
        
        #  SET STATE
        if message.text == 'value':
            await States.value.set()
        
        #  NEXT STATE
        if message.text == 'value':
            await States.next()
        







#  DELETE MESSAGE 1
async def delete_message_1(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    except:
        pass

#  DELETE MESSAGE 2
async def delete_message_2(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass

#  DELETE MESSAGE 3
async def delete_message_3(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 2)
    except:
        pass





#  ON START UP
async def start_bot(_):
    await bot.send_message(284929331, 'The bot is successfully enabled ✅')



#  LAUNCH THE BOT
if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates = True, on_startup = start_bot)
        except Exception as e:
            print(e)
            continue