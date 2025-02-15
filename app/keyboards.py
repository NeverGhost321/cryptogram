from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton  
from app.databases.requests import get_categories

from aiogram.utils.keyboard import InlineKeyboardBuilder
# Инлайн-кнопки (под сообщением)
main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="БАЗА за 39$ / мес.", callback_data="baza")],
    [InlineKeyboardButton(text="КЛУБ КИТОВ", callback_data="trial_by_shef")],
    [InlineKeyboardButton(text="Мои доступы", callback_data="my_access"), 
     InlineKeyboardButton(text="Контакты", callback_data="contacts")]
])

# Обычная (Reply) кнопка "🏚 Вернуться в меню"
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏚 Вернуться в меню")]],
    resize_keyboard=True
)

private_by_shef = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Месяц', callback_data='one_month'),
     InlineKeyboardButton(text='Квартал', callback_data='three_months')],  # Первая кнопка теперь занимает всю ширину
    [InlineKeyboardButton(text='Полгода', callback_data='six_months'),
     InlineKeyboardButton(text='Годовая', callback_data='subscribe_year')],  # Две кнопки в строке
    [InlineKeyboardButton(text='Навсегда', callback_data='subscribe_forever')],
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu')]
])
# Клавиатура выбора подписки
subscription_trial_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="квартал", callback_data="whales_three_month"),
        InlineKeyboardButton(text="полгода", callback_data="whales_six_month")
    ],
    [
        InlineKeyboardButton(text="Год", callback_data="whales_one_year"),
        InlineKeyboardButton(text="Навсегда", callback_data="whales_forever")
    ],
    [InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")]
])
# Клавиатура для подтверждения оплаты
confirm_payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Оплатил, отправить хеш", callback_data="send_payment_hash")],
    [InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_to_menu")]
])

# Создание инлайн-клавиатуры
bioacking_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="3 месяца", callback_data="subscribe_biohacking_three_months")],
    [InlineKeyboardButton(text="6 месяцев", callback_data="subscribe_biohacking_six_months")],
    [InlineKeyboardButton(text="Один год", callback_data="subscribe_biohacking_one_year")],
    [InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")]
])


# Обновленная клавиатура для подписки на 3 месяца
three_months_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_subscription_base")]
])

# Обновленная клавиатура для подписки на 6 месяцев
trial_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_subscription_trial")]
])
# Обновленная клавиатура для подписки на 6 месяцев
bioacking_cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_subscription_bioacking")]
])

# Клавиатура с пятью кнопками
personal_buttons_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🏛️ БАЗА", callback_data="base")],  # Кнопка "БАЗА" на отдельной строке
    [InlineKeyboardButton(text="🐋 КЛУБ КИТОВ", callback_data="whales_club")],  # Кнопка "КЛУБ КИТОВ" на отдельной строке
    [
        InlineKeyboardButton(text="Каналы", callback_data="channels"),
        InlineKeyboardButton(text="Курсы", callback_data="category_Курсы")
    ],
    [InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")]
])