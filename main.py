from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import *
from utils import *

bot = Bot(token='5418131806:AAE_J5DDjWvDByFqp_4GJ64hH3kOxL0DWCA')
dp = Dispatcher(bot, storage=MemoryStorage())  # May be used MongoDB, Redis etc.


def master_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Создать группу рабочих',
        'Назначить задание',
        'Получить отчёты'
    ]
    menu.add(*buttons)

    return menu


class User(StatesGroup):
    login = State()


class Master(StatesGroup):
    menu = State()
    create_group = State()
    adding_users_to_group = State()
    create_task = State()
    set_users_to_task = State()
    get_statistic = State()
    delete_group = State()


# Start
@dp.message_handler(commands=['start'])
async def start(msg: Message):
    await User.login.set()
    await msg.answer('Добро пожаловать в BuilderTaskTracker\nВпишите Ваш логин:', reply_markup=ReplyKeyboardRemove())


# Authentication user
@dp.message_handler(state=User.login)
async def login(msg: Message, state: FSMContext):
    login = msg.text
    print('Try to login:', login)
    if is_exist(login):
        id = get_user_id_by_login(login)
        role = get_role(id)
        fullname = get_fullname(id)
        if role == 'master':
            print(f'Success: Master {id}')
            await state.update_data(login=login, id=id)
            await Master.menu.set()

            await msg.answer(f'Добро пожаловать {fullname}', reply_markup=master_menu())
            return
        elif role == 'slave':
            print(f'Success: Slave {id}')
            pass
            return
    await msg.answer('Такой пользователь не найден')


# Master menu
@dp.message_handler(state=Master.menu)
async def master_menu(msg: Message, state: FSMContext):
    try:
        id = await state.get_data('id')
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    command = msg.text
    if command == 'Создать группу рабочих':
        await Master.create_group.set()
        await msg.answer('Введите название', reply_markup=ReplyKeyboardRemove())
    elif command == 'Назначить задание':
        await Master.create_task.set()
        # todo
        await msg.answer('В разработке', reply_markup=ReplyKeyboardRemove())
    elif command == 'Получить отчёты':
        await Master.get_statistic.set()
        # todo
        await msg.answer('В разработке', reply_markup=ReplyKeyboardRemove())


# Master create group
@dp.message_handler(state=Master.create_group)
async def master_create_group(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    token = create_token(msg.text + str(id))
    group_id = create_group(msg.text, token, id)
    await Master.menu.set()
    await msg.answer(f'Группа {msg.text} создана\nТокен: `{token}`', reply_markup=master_menu())


executor.start_polling(dp, skip_updates=True)
