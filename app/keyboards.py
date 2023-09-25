from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')

catalog_list = InlineKeyboardMarkup(row_width=3)
catalog_list.add(InlineKeyboardButton(text='Обычная тара', callback_data='Usual-bottles'),
                 InlineKeyboardButton(text='Особая тара', callback_data='Special-bottles'), )
