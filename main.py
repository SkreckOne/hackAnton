import datetime

from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import *
from utils import *
from sqlite3 import IntegrityError

bot = Bot(token='5418131806:AAE_J5DDjWvDByFqp_4GJ64hH3kOxL0DWCA')
dp = Dispatcher(bot, storage=MemoryStorage())  # May be used MongoDB, Redis etc.


class User(StatesGroup):
    login = State()


class Master(StatesGroup):
    menu = State()
    create_group = State()
    delete_group = State()
    adding_users_to_group = State()
    create_task = State()
    set_start_date = State()
    set_end_date = State()
    set_start_time = State()
    set_end_time = State()
    set_attr = State()
    set_group = State()
    set_users_to_task = State()
    get_statistic = State()


class Slave(StatesGroup):
    menu = State()
    join_group = State()


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
        role = get_role(login)
        fullname = get_fullname(login)
        if role == 'master':
            print(f'Success: Master {id}')
            await state.update_data(login=login, id=id)
            await Master.menu.set()

            menu = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                'Создать группу рабочих',
                'Посмотреть группы',
                'Удалить группу',
                'Назначить задание',
                'Получить отчёты'
            ]
            menu.add(*buttons)

            await msg.answer(f'Добро пожаловать, {fullname}', reply_markup=menu)
            return
        elif role == 'slave':
            print(f'Success: Slave {id}')
            await state.update_data(login=login, id=id)
            await Slave.menu.set()

            menu = ReplyKeyboardMarkup(resize_keyboard=True)
            menu.add('Присоединиться к группе')
            buttons = [
                'Посмотреть группу',
                'Посмотреть текущее задание',
            ]
            menu.add(*buttons)
            menu.add('Отправить отчёт об выполнении работ')

            await msg.answer(f'Добро пожаловать, {fullname}', reply_markup=menu)
            return
    await msg.answer('Такой пользователь не найден')


@dp.message_handler(commands=['exit'], state='*')
async def logout(msg: Message, state: FSMContext):
    await state.reset_state(False)
    await msg.answer('Вы вышли из системы.\nДо свидания!', reply_markup=ReplyKeyboardRemove())


# Master menu
@dp.message_handler(state=Master.menu)
async def master_menu(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    command = msg.text
    if command == 'Создать группу рабочих':
        await Master.create_group.set()
        await msg.answer('Введите название:', reply_markup=ReplyKeyboardRemove())
    elif command == 'Посмотреть группы':
        groups = get_masters_groups(id)
        if groups:
            for group in groups:
                count = count_slaves(group[0])
                group_name = group[1]
                token = group[3]
                await msg.answer(f'Группа {group_name}\nТокен: ** `{token}` **\nКоличество рабочих: {count}', parse_mode='Markdown')
        else:
            await msg.answer('Рабочих групп не создано')
    elif command == 'Удалить группу':
        await Master.delete_group.set()

        groups_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [group[1] for group in get_masters_groups(id)]
        for button in buttons:
            groups_buttons.add(button)
        await msg.answer('Выберите группу', reply_markup=groups_buttons)
    elif command == 'Назначить задание':
        await Master.create_task.set()
        pattern = ReplyKeyboardMarkup(resize_keyboard=True)
        pattern.add('Ремонт дороги')
        await msg.answer('Выберите шаблон', reply_markup=pattern)
    elif command == 'Получить отчёты':
        print('statistic')
        await Master.get_statistic.set()
        await msg.answer('Отчёты:')
        await master_get_statistic(msg, state)


# Master statistic
@dp.message_handler(state=Master.get_statistic)
async def master_get_statistic(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    print('temp')

    groups = get_masters_groups(id)
    print(groups)
    for group in groups:
        task = get_task_by_group_id(group[0])
        text = f'Группа: {group[1]}\n\n'
        text += f'Задача: {task[1]}\n\n'
        text += f'Степень выполнения: {count_done_slaves(group[0])}/{count_slaves(group[0])}'
        await msg.answer(text)
    await Master.menu.set()


# Master create task
@dp.message_handler(state=Master.create_task)
async def master_create_taks(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    command = msg.text

    if command == 'Ремонт дороги':
        await msg.answer('Шаблон: Ремонт дороги')
        await msg.answer('Необходимо провести ремонтные работы на проезжей части на улице <название улицы>\n' +
                         'Работы проводятся ежедневно с <начало рабочего дня> до <конец рабочего дня>.\n' +
                         'Период работы с <дата начала> по <дата окончания>')
        await Master.set_start_time.set()
        await msg.answer('Впишите время начала рабочего дня', reply_markup=ReplyKeyboardRemove())
    else:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            'Создать группу рабочих',
            'Посмотреть группы',
            'Удалить группу',
            'Назначить задание',
            'Получить отчёты'
        ]
        menu.add(*buttons)
        await Master.menu.set()
        await msg.answer('Шаблон не найден', reply_markup=menu)


# Master set start time
@dp.message_handler(state=Master.set_start_time)
async def master_set_start_time(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    time = msg.text
    await state.update_data(start_time=time)
    await Master.set_end_time.set()
    await msg.answer('Введите время окончания рабочего дня')


# Master set end time
@dp.message_handler(state=Master.set_end_time)
async def master_set_end_time(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    time = msg.text
    await state.update_data(end_time=time)
    await Master.set_start_date.set()
    await msg.answer('Введите дату начала работ')


# Master set start date
@dp.message_handler(state=Master.set_start_date)
async def master_set_start_date(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    date = msg.text
    await state.update_data(start_date=date)
    await Master.set_end_date.set()
    await msg.answer('Введите дату окончания работ')


# Master set end date
@dp.message_handler(state=Master.set_end_date)
async def master_set_end_date(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    date = msg.text
    await state.update_data(end_date=date)
    await Master.set_attr.set()
    await msg.answer('Введите дополнительные сведения (адрес или тп.)')


# Master set attr
@dp.message_handler(state=Master.set_attr)
async def master_set_attr(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    attr = msg.text
    await state.update_data(attr=attr)
    await Master.set_group.set()

    groups_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [group[1] for group in get_masters_groups(id)]
    for button in buttons:
        groups_buttons.add(button)

    await msg.answer('Выберите группу для выполнения', reply_markup=groups_buttons)


# Master set group to task
@dp.message_handler(state=Master.set_group)
async def master_set_group(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Создать группу рабочих',
        'Посмотреть группы',
        'Удалить группу',
        'Назначить задание',
        'Получить отчёты'
    ]
    menu.add(*buttons)

    group = msg.text
    if group not in [group[1] for group in get_masters_groups(id)]:
        groups_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [group[1] for group in get_masters_groups(id)]
        for button in buttons:
            groups_buttons.add(button)

        await msg.answer('Выберите группу для выполнения', reply_markup=groups_buttons)
        return

    group_id = get_group_id_by_name(group)
    data = await state.get_data()
    date_start = data['start_date']
    date_end = data['end_date']
    time_start = data['start_time']
    time_end = data['end_time']
    text = data['attr']

    final_text = f'Необходимо провести ремонтные работы на проезжей части на улице {text}\n' + \
    f'Работы проводятся ежедневно с {time_start} до {time_end}.\n' + \
    f'Период работы с {date_start} по {date_end}'

    try:

        create_task(final_text, date_start, date_end, time_start, time_end, id, group_id)
    except Exception as e:
        print(e)

        await msg.answer(f'Ошибка', reply_markup=menu)
    else:
        await msg.answer('Успешно создано', reply_markup=menu)
    await Master.menu.set()


# Slave menu
@dp.message_handler(state=Slave.menu)
async def slave_menu(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    command = msg.text

    if command == 'Присоединиться к группе':
        await Slave.join_group.set()
        await msg.answer('Введите токен', reply_markup=ReplyKeyboardRemove())
    elif command == 'Посмотреть группу':
        slave = get_slave(id)
        slaves = get_group_slaves(slave[3])
        await msg.answer('Ваша группа:')
        await msg.answer('\n'.join([slave[2] for slave in slaves]))
    elif command == 'Посмотреть текущее задание':
        pass
    elif command == 'Отправить отчёт об выполнении работ':
        pass


# Slave join group
@dp.message_handler(state=Slave.join_group)
async def slave_join_group(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add('Присоединиться к группе')
    buttons = [
        'Посмотреть группу',
        'Посмотреть текущее задание',
    ]
    menu.add(*buttons)
    menu.add('Отправить отчёт об выполнении работ')

    token = msg.text
    group = get_group_by_token(token)
    if not group:
        await msg.answer('Группа не найдена', reply_markup=menu)
    else:
        set_salve_to_group(group[0], id)
        await msg.answer(f'Вы успешно добавились в группу', reply_markup=menu)
    await Slave.menu.set()


# Master create group
@dp.message_handler(state=Master.create_group)
async def master_create_group(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Создать группу рабочих',
        'Посмотреть группы',
        'Удалить группу',
        'Назначить задание',
        'Получить отчёты'
    ]
    menu.add(*buttons)

    token = create_token(msg.text + str(id))
    try:
        group_id = create_group(msg.text, token, id)
    except IntegrityError as e:
        await msg.answer('Группа с таким название существует', reply_markup=menu)
    except Exception as e:
        print(e)
        await msg.answer('Непридвиденная ошибка во время создания', reply_markup=menu)
    else:
        await msg.answer(f'Группа {msg.text} создана\nТокен: ** `{token}` **', reply_markup=menu, parse_mode='Markdown')
    await Master.menu.set()


# Master delete group
@dp.message_handler(state=Master.delete_group)
async def master_delete_group(msg: Message, state: FSMContext):
    try:
        id = (await state.get_data())['id']
    except Exception as e:
        print(e)
        await state.reset_state(False)
        await msg.answer('Не авторризован. Введите /start')

    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        'Создать группу рабочих',
        'Посмотреть группы',
        'Удалить группу',
        'Назначить задание',
        'Получить отчёты'
    ]
    menu.add(*buttons)

    group_id = get_group_id_by_name(msg.text)
    if group_id == -1:
        await msg.answer('Используйте клавишы для ввода')
        return
    try:
        delete_group(group_id)
    except Exception as e:
        await msg.answer('Ошибка удаления', reply_markup=menu)
    else:
        await msg.answer('Успешно удалено', reply_markup=menu)
    await Master.menu.set()


executor.start_polling(dp, skip_updates=True)
