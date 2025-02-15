import asyncio
import pathlib
import pickle
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
import logging
import re  # Импортируем модуль для работы с регулярными выражениями

# Функция для проверки корректности HTML-разметки
def is_valid_html(text):
    try:
        # Ищем все открывающие теги
        open_tags = re.findall(r'<(\w+)[^>]*>', text)
        # Ищем все закрывающие теги
        close_tags = re.findall(r'</(\w+)>', text)

        # Проверяем, что для каждого открывающего тега есть закрывающий
        for tag in open_tags:
            if close_tags.count(tag) < open_tags.count(tag):
                return False, f"Не хватает закрывающего тега </{tag}>"
        return True, None
    except Exception as e:
        # Если возникает ошибка, разметка некорректна
        logging.error(f"Ошибка в HTML-разметке: {e}")
        return False, "Ошибка при проверке HTML-разметки."

root_path = pathlib.Path(__file__).parent.resolve()

# Загрузка данных из файлов
try:
    with open(f'{root_path}/blacklist.pkl', 'rb') as f:
        blacklist = pickle.load(f)
except:
    blacklist = []

try:
    with open(f'{root_path}/text_main.pkl', 'rb') as f:
        text_main = pickle.load(f)
except:
    text_main = {'text': 'Тестовый текст', 'photo': None}

# Настройки
channel_id_main = '-1002350020257'  # ID вашего канала
admins = ['1004305901', '1107486256']  # Айди админов
token = '6786983737:AAEWM03ZgqW37Z-VPTCuuO-xfhFDFBHCMnQ'

# Создание класса состояний для FSM
class fsm_data(StatesGroup):
    text_state = State()

# Создание бота и диспетчера
bot = Bot(token=token)
storage = MemoryStorage()  # создаем объект хранилища
dp = Dispatcher(storage=storage)  # инициализируем диспетчер

cancel_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Отмена')]
    ]
)

# Обработчик команды /text
@dp.message(Command("text"))
async def func(message: types.Message, state: FSMContext):
    global text_main
    print(f"Пользователь {message.from_user.id} вызвал команду /text")
    if str(message.from_user.id) in admins:
        try:
            await state.clear()  # Очистка состояния
        except:
            pass
        await message.answer(
            f'Введите новый текст и вставьте фото (при необходимости)\nСейчас текст:\n{text_main["text"]}',
            reply_markup=cancel_kb,
            parse_mode='HTML'
        )
        await state.set_state(fsm_data.text_state)
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.message(fsm_data.text_state)
async def handle_text_and_media(message: types.Message, state: FSMContext):
    global text_main
    if str(message.from_user.id) in admins:
        if str(message.text).lower() == 'отмена':
            await state.clear()
            await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())
        else:
            # Если это текстовое сообщение
            if message.text:
                # Проверяем корректность HTML-разметки
                is_valid, error_message = is_valid_html(message.text)
                if is_valid:
                    text_main['text'] = message.text
                    text_main['photo'] = None
                else:
                    await message.answer(f'Ошибка: {error_message}')
                    return

            # Если это медиа-сообщение (фото с подписью)
            elif message.photo:
                caption = message.caption if message.caption else ""
                # Проверяем корректность HTML-разметки в подписи
                is_valid, error_message = is_valid_html(caption)
                if is_valid:
                    text_main['text'] = caption
                    text_main['photo'] = message.photo[-1].file_id
                else:
                    await message.answer(f'Ошибка: {error_message}')
                    return

            # Сохраняем изменения в файл
            with open(f'{root_path}/text_main.pkl', 'wb') as f:
                pickle.dump(text_main, f)

            await message.answer('Текст и/или фото были изменены', reply_markup=types.ReplyKeyboardRemove())
            await state.clear()

# Обработчик всех сообщений
@dp.message()
async def starter(message: types.Message):
    global text_main, blacklist
    try:
        print(f"ID канала: {message.chat.id}")
        print(f"ID отправителя: {message.from_user.id}")
        print(f"ID sender_chat: {message.sender_chat.id if message.sender_chat else 'Нет sender_chat'}")

        # Проверка, что сообщение пришло из нужного канала и от пользователя 777000
        if message.from_user.id == 777000 and message.sender_chat and message.sender_chat.id == int(channel_id_main):
            media_id = getattr(message, 'media_group_id', '')
            if media_id and media_id not in blacklist:
                blacklist.add(media_id)
                with open(f'{root_path}/blacklist.pkl', 'wb') as f:
                    pickle.dump(blacklist, f)

            # Проверяем корректность HTML-разметки перед отправкой
            is_valid, error_message = is_valid_html(text_main['text'])
            if is_valid:
                if not text_main['photo']:
                    # Используем send_message для отправки комментария
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=text_main['text'],
                        parse_mode='HTML',
                        disable_web_page_preview=True,
                        reply_to_message_id=message.message_id  # Ответ на конкретное сообщение
                    )
                else:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=text_main['photo'],
                        caption=text_main['text'],
                        parse_mode='HTML',
                        reply_to_message_id=message.message_id  # Ответ на конкретное сообщение
                    )
            else:
                # Уведомляем администратора об ошибке
                for admin in admins:
                    await bot.send_message(
                        chat_id=admin,
                        text=f"Ошибка в тексте: {error_message}\nТекст: {text_main['text']}"
                    )
    except Exception as e:
        print(f"Ошибка: {e}")

# Функция для запуска бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())