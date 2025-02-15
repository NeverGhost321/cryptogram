import asyncio
import time
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ChatJoinRequest
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import update
from datetime import datetime
from app.handlers import router
from app.databases.models import async_session, UserSubscription, Item, TelegramChannel, SubscriptionType
import logging

from aiogram import types

from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton  

from app.handlers import router
logging.basicConfig(level=logging.INFO)

async def get_user_subscription_category(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(UserSubscription)
            .options(joinedload(UserSubscription.item))
            .where(
                UserSubscription.user_id == user_id,
                UserSubscription.status == 'active'
            )
        )
        subscriptions = result.scalars().all()

        # Используем SubscriptionType для точного сравнения
        categories = {sub.item.type for sub in subscriptions}  
        return categories  # Вернёт Enum SubscriptionType

async def get_allowed_channels(subscription_categories):
    async with async_session() as session:
        result = await session.execute(select(TelegramChannel))
        channels = result.scalars().all()

        allowed_channels = []
        for channel in channels:
            if SubscriptionType.Whales_club in subscription_categories:
                allowed_channels.append(channel.channel_id)
            elif SubscriptionType.Base in subscription_categories and channel.type_sub != 'Whales_club_only':
                allowed_channels.append(channel.channel_id)

        return allowed_channels

async def check_subscriptions():
    """Проверяет подписки пользователей и обновляет их статус, если подписка истекла."""
    async with async_session() as session:
        # Получаем все активные подписки
        result = await session.execute(
            select(UserSubscription)
            .where(UserSubscription.status == 'active')
        )
        subscriptions = result.scalars().all()

        for subscription in subscriptions:
            if subscription.end_date and subscription.end_date <= datetime.now():
                # Обновляем статус подписки на inactive
                await session.execute(
                    update(UserSubscription)
                    .where(UserSubscription.id == subscription.id)
                    .values(status='inactive')
                )
                await session.commit()

                # Исключаем пользователя из каналов
                await remove_user_from_channels(subscription.user_id)

async def remove_user_from_channels(user_id: int):
    """Исключает пользователя из всех каналов."""
    async with async_session() as session:
        # Получаем все каналы, в которых состоит пользователь
        result = await session.execute(
            select(TelegramChannel)
            .join(UserSubscription)
            .where(UserSubscription.user_id == user_id)
        )
        channels = result.scalars().all()

        bot = Bot.get_current()
        for channel in channels:
            try:
                await bot.ban_chat_member(chat_id=channel.channel_id, user_id=user_id)
                logging.info(f"Пользователь {user_id} исключён из канала {channel.channel_id}")
            except Exception as e:
                logging.error(f"Ошибка при исключении пользователя {user_id} из канала {channel.channel_id}: {e}")

async def schedule_subscription_check():
    """Запускает проверку подписок каждые 24 часа."""
    while True:
        await check_subscriptions()
        await asyncio.sleep(86400)  # 24 часа
        
           
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

async def send_welcome_message(bot: Bot, user_id: int, username: str):
    # Первое сообщение с изображением и текстом
    text = (
        f"Алоха, {username}\n\n"
        "<b>Всего 3 минуты.</b>\n"
        "<i>Каких-то 180 секунд…</i>\n\n"
        "За которые ты успеешь подробно узнать, куда же ты попал, и как заработать на этом от +427%.\n"
        "<b>От ненужной лирики, к делу 👇🏽</b>\n\n"
        "<b>ФАКТ #1</b> — я трачу более 217.000$ ежегодно, скупая лучшие крипто и инвест подписки: клубы, инсайды, "
        "обучения, доступы к сервисам и дорогостоящим платформам.\n\n"
        "Частью этой информации я бесплатно делюсь со своими подписчиками в канале. За последний год ты мог сделать "
        "от +427% тупо повторяя за мной.\n\n"
        "<b>ФАКТ #2</b> — полноценный доступ ко всей инсайд.информации ты можешь получить в моей <a href='https://t.me/cclub'><b>БАЗЕ</b></a> "
        "всего за 39$ / мес (символическая цена, чтобы отсеять нахлебников).\n\n"
        "<b>ФАКТ #3</b> — мой бесплатный канал априори закрывает абсолютно все запросы стандартного криптана: сделки, "
        "новости, инвест-идеи, инсайды по монетам, политика.\n"
        "Обязательно закрепи его у себя."
    )

    # Отправляем первое сообщение с картинкой
    message = await bot.send_photo(
        chat_id=user_id,
        photo=FSInputFile('image/welcome.jpg'),
        caption=text,
        parse_mode="HTML"
    )

    # Клавиатура с кнопкой "Запустить бота"
    start_button = InlineKeyboardButton(text="ЗАПУСТИТЬ БОТА", callback_data="start_bot")
    start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[start_button]])

    # Второе сообщение с важными сюжетками, отвечая на первое
    second_text = (
        "<b>ВАЖНЫЕ СЮЖЕТКИ ИЗ КАНАЛА</b>\n"
        "<i>Советую ознакомиться перед тем, как ты начнешь торговлю:</i>\n\n"
        "• Моя личная история 🤫\n"
        "• Как я сделал +427% за год, уделяя всего 15 минут в день.\n"
        "• Фактическое доказательство моих иксов (реальная статистика).\n"
        "• Как подписчик заработал на BMW X5 COMPETITION (160.000$).\n"
        "• +7.000$ как с куста, или 'как получить в управление 500.000$'.\n"
        "• Политика, мироустройство, инсайды — как всё это связано с криптой и финансовыми рынками?\n"
        "<i>(ссылки на посты в доработке)</i>\n\n"
        "Чтобы запустить бота — жми на кнопку /start ниже, welcome 👇🏽"
    )

    # Отправляем второе сообщение как ответ на первое
    await bot.send_message(
        chat_id=user_id,
        text=second_text,
        reply_to_message_id=message.message_id,  # Ответ на предыдущее сообщение
        reply_markup=start_keyboard
    )

    
async def main():
    bot = Bot(
        token='6786983737:AAEWM03ZgqW37Z-VPTCuuO-xfhFDFBHCMnQ',
        default=DefaultBotProperties(parse_mode='HTML')
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    @dp.chat_join_request()
    async def approve_join_request(update: ChatJoinRequest):
        user_id = update.from_user.id  
        chat_id = update.chat.id
        username = update.from_user.username or update.from_user.first_name
        logging.info(f"Запрос на вступление от пользователя {user_id} в канал {chat_id}")

        # Если заявка отправляется в канал с ID -1002033938511, автоматически одобряем
        if chat_id == -1002033938511:
            logging.info(f"АВТОМАТИЧЕСКОЕ ОДОБРЕНИЕ заявки для {user_id} в {chat_id}")
            await update.approve()  # Одобряем заявку
            await send_welcome_message(bot, user_id, username)  # Отправляем приветственное сообщение
            return  # Завершаем выполнение функции, чтобы не проверять подписку

        # Обычная логика для других каналов
        user_categories = await get_user_subscription_category(user_id)
        logging.info(f"Категории подписок пользователя: {user_categories}")

        if not user_categories:
            await bot.send_message(user_id, "У вас нет активной подписки для вступления в канал.")
            return

        allowed_channels = await get_allowed_channels(user_categories)
        logging.info(f"Доступные каналы: {allowed_channels}")

        if abs(chat_id) in allowed_channels:
            logging.info(f"ОДОБРЯЕМ заявку для {user_id} в {chat_id}")
            await update.approve()
            await bot.send_message(user_id, "Ваша заявка принята!")
        else:
            logging.info(f"ОТКАЗ пользователю {user_id} в {chat_id}")
            await bot.send_message(user_id, "У вас нет доступа к этому каналу.")

    # Запускаем проверку подписок в фоновом режиме
    asyncio.create_task(schedule_subscription_check())
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())