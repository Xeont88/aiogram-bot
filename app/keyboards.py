from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку').add('Назад')

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Обычная тара', callback_data='Usual-bottles'),
                 InlineKeyboardButton(text='Особая тара', callback_data='Special-bottles'), )


cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(InlineKeyboardButton(text='Отмена', callback_data='Отмена'))


async def create_items_kb(items: list):
    items_kb = InlineKeyboardMarkup(row_width=3)
    for item in items:
        items_kb.add(InlineKeyboardButton(text=item[0], callback_data=item[0]))
    return items_kb