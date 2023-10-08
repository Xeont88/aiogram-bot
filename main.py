from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os
import app.stickers as st_s

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)
admins_list = [int(i) for i in os.getenv('ADMIN_ID').split(',')]


# Запуск бота
async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')


# Класс состояний этапов заказа
class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    # photo = State()


# Обработка запуска бота пользователем
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker(st_s.greeting_sticker)
    if message.from_user.id in admins_list:
        await message.answer(f'Привет админ, {message.from_user.first_name}!', reply_markup=kb.main_admin)
    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать в бот для приема заявок!',
                             reply_markup=kb.main)


# Открываем меню каталога
@dp.message_handler(text='Каталог')
async def cart(message: types.Message):
    await message.answer(f'Каталог:', reply_markup=kb.catalog_list)
    items = await db.get_items()
    items_kb = await kb.create_items_kb(items)
    await message.answer(f'Список товаров:', reply_markup=items_kb)


# Открываем меню корзины
@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')


# # Выводим id пользователя, при команде id
# @dp.message_handler(text='id')
# async def cart(message: types.Message):
#     await message.answer(f'{message.from_user.id}')


# Вывод админ панели (только для админов)
@dp.message_handler(text='Админ панель')
async def cart(message: types.Message):
    if message.from_user.id in admins_list:
        await message.answer(f'АД-минка!', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю ...')


# Выход из админ панели
@dp.message_handler(text='Назад')
async def cart(message: types.Message):
    if message.from_user.id in admins_list:
        # await NewOrder.previous()
        await message.answer(f'Назад', reply_markup=kb.main_admin)
    else:
        await message.reply('Я тебя не понимаю ...')


# Отмена создания товара
@dp.message_handler(text='Отмена')
async def cart(message: types.Message):
    if message.from_user.id in admins_list:
        # await NewOrder.previous()
        await message.answer(f'Назад', reply_markup=kb.main_admin)
    else:
        await message.reply('Я тебя не понимаю ...')


@dp.message_handler(text='Добавить товар')
async def cart(message: types.Message):
    if message.from_user.id in admins_list:
        await NewOrder.type.set()
        await message.answer(f'Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю ...')


@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer(f'Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(f'Напишите описание товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer(f'Напишите цену товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_item_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    # await message.answer(f'Отправьте фотографию товара')
    # await NewOrder.next()
    await db.add_item(state)
    await message.answer(f'Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()


# @dp.message_handler(lambda message: not message.photo, state=NewOrder.price)
# async def add_item_photo(message: types.Message):
#     await message.answer("Это не фотография!")


# @dp.message_handler(content_types=['photo'], state=NewOrder.photo)
# async def add_item_photo(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['photo'] = message.photo[0].file_id
#     await db.add_item(state)
#     await message.answer(f'Товар успешно создан!', reply_markup=kb.admin_panel)
#     await state.finish()


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
