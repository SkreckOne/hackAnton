from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from db import *

bot = Bot(token='5418131806:AAE_J5DDjWvDByFqp_4GJ64hH3kOxL0DWCA')
dp = Dispatcher(bot)


class User(StatesGroup):
    login = State()


class Master(StatesGroup):
    menu = State()
    create_group = State()
    adding_users_to_group = State()
    create_task = State()
    set_users_to_task = State()
    get_feedback = State()
    delete_group = State()



@dp.message_handler(commands=['start'])
async def start(msg: Message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Вход')
    await msg.answer('Добро пожаловать в BuilderTaskTracker', reply_markup=markup)


@dp.message_handler(state=User.login)
async def login(msg: Message, state: FSMContext):
    login = msg.text
    if True: # Check for existing user
        await state.set_data(login=login)
        await Master.menu.set()
    else:
        await msg.answer('Такой пользователь не найден')



executor.start_polling(dp, skip_updates=True)

print('Complete')
