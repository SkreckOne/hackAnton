from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message
from requestlib import get


bot = Bot(token='5418131806:AAE_J5DDjWvDByFqp_4GJ64hH3kOxL0DWCA')
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def popug(msg: Message):
    res = get('https://02.letoctf.cbap.ru/webapi/Account').text
    await msg.answer(res)


executor.start_polling(dp, skip_updates=True)
