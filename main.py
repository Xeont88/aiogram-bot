from aiogram import Bot, Dispatcher, types, executor
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAIB62URx90LvAIrSM6ystcub2xoULrPAAIFAAPANk8T-WpfmoJrTXUwBA')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в бот для приема заявок!',
                         reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Привет админ!', reply_markup=kb.main_admin)


@dp.message_handler(text='Каталог')
async def cart(message: types.Message):
    await message.answer(f'Каталог:', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')


@dp.message_handler(text='id')
async def cart(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='Админ панель')
async def cart(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'АД-минка!', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю ...')


# @dp.message_handler(content_types=['sticker'])
# async def check_sticker(message: types.Message):
#     await message.answer(message.sticker.file_id)
#     await bot.send_message(message.from_user.id, message.chat.id)


# @dp.message_handler(content_types=['document', 'photo'])
# async def forward_message(message: types.Message):
#     await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю ...')


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'Usual-bottles':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали "Обычная тара"')
    elif callback_query.data == 'Special-bottles':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали "Особая тара"')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    # executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
