from datetime import datetime
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy import select, update
from aiogram.types import FSInputFile

from aiogram.utils.markdown import hlink
import app.keyboards as kb
import app.databases.requests as rq
from app.databases.models import Item, SubscriptionDuration, UserSubscription, TelegramChannel, SubscriptionType
from datetime import datetime, timedelta
from app.databases.models import async_session, User
from app.keyboards import three_months_keyboard, trial_keyboard, subscription_trial_keyboard, bioacking_keyboard, bioacking_cancel_keyboard, personal_buttons_keyboard
import requests

from aiogram.types import ChatJoinRequest

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select, distinct
from app.databases.models import async_session 

from aiogram import Bot


router = Router()

@router.callback_query(F.data == "start_command")
async def start_callback(call: CallbackQuery):
    await call.message.delete()  # Удаляем сообщение с кнопкой (если нужно)
    await call.bot.send_message(call.from_user.id, "/start")  # Отправляем команду /start

# Определяем функцию hbold
def hbold(text: str) -> str:
    return f"<b>{text}</b>"

# Определяем функцию hlink
def hlink(text: str, url: str) -> str:
    return f'<a href="{url}">{text}</a>'

# Общая функция для отправки сообщения "baza"
async def send_baza_message(target: types.Message | types.CallbackQuery):
    caption_text = (
        "<b>РАЗДАЮ АБСОЛЮТНО ВСЕ ПРИВАТКИ ЗА <s>150.000$</s> 39$😱</b>\n\n"
        "Кратко о том, что внутри:\n"
        "<b>• 50+ ПРИВАТОК:</b> доступ ко всем эксклюзивным материалам общей стоимостью 150.000$+ в год\n"
        "<b>• БАЗА ОБУЧЕНИЙ:</b> более 30 курсов по крипте и инвестициям\n"
        "(всегда пополняю ассортимент)\n"
        "<b>• ПОДСВЕЧЕННЫЕ ИДЕИ:</b> мой авторский канал с отборными сделками и инсайдами (личная статистика более +427% / год)\n"
        "<b>• АЛГОТРЕЙДИНГ:</b> возможность делать гарантированные +140% годовых на абсолютном пассиве\n"
        "<b>• ЧАТ КОММЬЮНИТИ:</b> общение, нетворкинг, взаимопомощь и дайджесты по всем приваткам\n"
        "<b>• МЕМКОИНЫ НА х1000:</b> хорошая возможность быстро раскачать свой небольшой депозит\n\n"
        "🎁 Общий созвон на тему стратегии заработка в рынке, которая принесла мне более 393.000$ за 2024 год!\n\n"
        "Подробная презентация в отдельном канале 👉🏽 <a href='https://t.me/clubkitov'><b>ТЫК</b></a>\n\n"
        "<b>💵 СТОИМОСТЬ ДОСТУПА:</b>\n\n"
        "1 месяца — <b>39$</b>\n"
        "3 месяца — <b>99$</b>\n"
        "6 месяцев — <b>179$</b>\n"
        "12 месяцев — <b>349$</b>\n"
        "Навсегда — <b>999$</b>\n\n"
        "Итог: делаешь всё по моей инструкции – зарабатываешь\nот 1000$ за 30 дней. ЖМИ 👇🏽"
    )


    # Если это CallbackQuery, используем message для ответа
    if isinstance(target, types.CallbackQuery):
        message = target.message
    else:
        message = target

    # Отправка фото с новым текстом и клавиатурой
    await message.answer_photo(
        photo=FSInputFile('image/collage/collage.jpg'),
        caption=caption_text,
        reply_markup=kb.private_by_shef,
        parse_mode="HTML"  # Указываем, что текст содержит HTML-разметку
    )

    # Если это CallbackQuery, подтверждаем обработку нажатия кнопки
    if isinstance(target, types.CallbackQuery):
        await target.answer()

# Общая функция для отправки сообщения "clubkitov"
async def send_clubkitov_message(target: types.Message | types.CallbackQuery):
    text = (
        "<b>КЛУБ КИТОВ™ — by @glavcom</b>\n\n"
        "Моё сообщество для людей с мозгами (и депозитом), где я транслирую персональный\n"
        "путь к цели в 100.000.000$\n\n"
        "Топовые юристы, лучшие\n"
        "врачи, киты, бизнесмены,\n"
        "CEO компаний и инвесторы\n\n"
        "<i>(любой жизненный вопрос можно будет решить в рамках 1-го чата)</i>\n\n"
        "• Доступ к материалам общей стоимостью 250.000$/год: клубы, курсы, инсайды, платные сервисы, инвестиционные отчеты и прочее\n"
        "• Мой авторский канал: сделки\n"
        "со статистикой +640%, мысли\n"
        "по рынку, инсайды, политика и обсуждение тем, про которые нельзя говорить вслух 🤫\n"
        "<b>• ЭКСКЛЮЗИВНЫЕ</b> инвест-темы\n"
        "с потенциалом на х10: ton номера, спекуляция NFT, снайпинг щитков\n"
        "• Мое авторское обучение основанное на личном 5\n"
        "летнем рыночном опыте\n"
        "<b>• ЖИРНЕЙШИЙ</b> чат с авторскими ветками и материалами: форекс, биохакинг, мироустройство\n\n"
        "🏛️ <b>Инвест фонд:</b> возможность делать гарантированные\n"
        "~40% годовых в баксе.\n\n"
        "💵 <b>СТОИМОСТЬ ДОСТУПА:</b>\n\n"
        "3 месяца — <b>299$</b>\n"
        "6 месяцев — <b>499$</b>\n"
        "12 месяцев — <b>999$</b>\n"
        "Навсегда — <b>2999$</b>\n\n"
        "Подробная презентация в отдельном канале 👉🏽 <a href='https://t.me/clubkitov'><b>ТЫК</b></a>"
    )

    # Если это CallbackQuery, используем message для ответа
    if isinstance(target, types.CallbackQuery):
        message = target.message
    else:
        message = target

    # Отправка фото с текстом и клавиатурой
    await message.answer_photo(
        photo=FSInputFile('image/whale.png'),
        caption=text,
        reply_markup=subscription_trial_keyboard,
        parse_mode="HTML"  # Указываем, что текст содержит HTML-разметку
    )

    # Если это CallbackQuery, подтверждаем обработку нажатия кнопки
    if isinstance(target, types.CallbackQuery):
        await target.answer()


# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    start_param = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ""

    if start_param == "baza":
        # Если параметр равен "baza", вызываем общую функцию
        await send_baza_message(message)
        
    elif start_param == "clubkitov":
        # Если параметр равен "clubkitov", вызываем функцию для отправки сообщения
        await send_clubkitov_message(message)
    else:
        # Если параметра нет, выполняем стандартное действие
        user_name = message.from_user.first_name  # Получаем имя пользователя
        caption_text = (
            f"<b>⛩️ × {user_name}, здравия желаю!</b>\n\n"
            "Я ежегодно трачу 150.000$+ \n"
            "выкупая различные инсайды, приватные клубы, обучения, отчеты и доступы к лучшим аналитикам по крипте и инвестициям. Частью этого\n"
            "материала я делюсь бесплатно.\n\n"
            f"За последний год ты мог сделать +427% тупо повторяя сделки и рекомендации из {hlink('канала', 'https://t.me/+Gs7mmvpSKaBkOGMy')} 🤝🏽\n\n"
            f"<b>КУДА ТЫ ПОПАЛ?</b>\n"
            "Это мой бот, который будет слать тебе часть этих ценных уроков, сигналов и инсайдов 365 дней \n"
            "в году абсолютно бесплатно.\n\n"
            f"39$ — цена полного доступа ко всем материалам: <b>ЖМИ НА КНОПКИ НИЖЕ 👇🏽</b>\n\n"
            f"<blockquote><b>🔗 ЧТО ТАКОЕ БАЗА?</b> — @CCLUB\n🔗 <b>ПРО КЛУБ КИТОВ</b> — @CLUBKITOV</blockquote>\n\n"
        )
        # Отправка фото и сообщения
        await message.answer_photo(
            photo=FSInputFile('image/welcome.png'),
            caption=caption_text,
            reply_markup=kb.main,  # Добавляем инлайн-кнопки (под фото)
            parse_mode="HTML"  # Указываем, что текст содержит HTML-разметку
        )


@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback_query: CallbackQuery):
     
    
    user_name = callback_query.from_user.first_name  # Получаем имя пользователя
    caption_text = (
                f"<b>⛩️ × {user_name}, здравия желаю!</b>\n\n"
                "Я ежегодно трачу 150.000$+ \n"
                "выкупая различные инсайды, приватные клубы, обучения, отчеты и доступы к лучшим аналитикам по крипте и инвестициям. Частью этого\n"
                "материала я делюсь бесплатно.\n\n"
                f"За последний год ты мог сделать +427% тупо повторяя сделки и рекомендации из {hlink('канала', 'https://t.me/+Gs7mmvpSKaBkOGMy')} 🤝🏽\n\n"
                f"<b>КУДА ТЫ ПОПАЛ?</b>\n"
                "Это мой бот, который будет слать тебе часть этих ценных уроков, сигналов и инсайдов 365 дней \n"
                "в году абсолютно бесплатно.\n\n"
                f"39$ — цена полного доступа ко всем материалам: <b>ЖМИ НА КНОПКИ НИЖЕ 👇🏽</b>\n\n"
                f"<blockquote><b>🔗 ЧТО ТАКОЕ БАЗА?</b> — @CCLUB\n🔗 <b>ПРО КЛУБ КИТОВ</b> — @CLUBKITOV</blockquote>\n\n"
            )
    # Удаляем текущее сообщение, чтобы избежать спама
    await callback_query.message.delete()

    # Отправка нового сообщения
    await callback_query.message.answer_photo(
        photo=types.FSInputFile('image/welcome.png'),
        caption=caption_text,
        reply_markup=kb.main,  # Основная клавиатура
        parse_mode="HTML"
    )

    await callback_query.answer()



# Обработчик для кнопки "📦 PRIVATE by Шеф"
@router.callback_query(lambda c: c.data == "baza")
async def private_by_shef(callback_query: CallbackQuery):
 
    # Вызываем общую функцию для отправки сообщения
    await send_baza_message(callback_query)


def get_tron_transaction(tx_hash):
    url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx_hash}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        token_transfers = data.get("tokenTransferInfo", {})
        to_address = token_transfers.get("to_address", "Не найдено")
        amount = token_transfers.get("amount_str", "Не найдено")
        print(f"Адрес получателя: {to_address}, Сумма: {amount}")
        
        # Преобразуем сумму в обычные доллары (делим на 1,000,000)
        if amount != "Не найдено":
            # Переводим в доллары, учитывая возможный курс (по умолчанию 1 USDT = 1 доллар)
            amount_in_dollars = int(amount) / 1000000  # Переводим в доллары
            return to_address, amount_in_dollars
        
    return None, None


# Создаем состояние для хранения выбранного item_id
class SubscriptionState(StatesGroup):
    selected_item = State()
    
    
@router.callback_query(lambda c: c.data == "one_month")
async def buy_one_month(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(selected_item=1)
    await handle_subscription(callback_query, item_id=1)
    
@router.callback_query(lambda c: c.data == "three_months")
async def buy_one_month(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=11)
    await handle_subscription(callback_query, item_id=11)

@router.callback_query(lambda c: c.data == "six_months")
async def buy_six_months(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=2)
    await handle_subscription(callback_query, item_id=2)

@router.callback_query(lambda c: c.data == "subscribe_year")
async def buy_one_year(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=3)
    await handle_subscription(callback_query, item_id=3)

@router.callback_query(lambda c: c.data == "subscribe_forever")
async def buy_forever(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=4)
    await handle_subscription(callback_query, item_id=4)

async def handle_subscription(callback_query: CallbackQuery, item_id: int):
    # Получаем нужный товар из базы данных по item_id
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.id == item_id))

        if item:
            # Рассчитываем дату окончания подписки в зависимости от её длительности
            duration_map = {
                SubscriptionDuration.one_month: timedelta(days=30),
                SubscriptionDuration.three_months: timedelta(days=90),
                SubscriptionDuration.six_months: timedelta(days=180),
                SubscriptionDuration.one_year: timedelta(days=365),
                SubscriptionDuration.forever: None
            }

            end_date = None
            if item.duration != SubscriptionDuration.forever:
                end_date = (datetime.now() + duration_map[item.duration]).strftime('%d.%m.%y')
            else:
                end_date = "Навсегда"

            # Выводим информацию о сумме, которую ожидаем
            print(f"Ожидаемая сумма для подписки '{item.name}': {item.price}$")

            # Генерация текста для ответа пользователю
            text = (
                "💸 | Информация о покупке\n\n"
                f"📌 Продукт: <b>{item.name}</b>\n"
                f"💰 К оплате: <b>{int(item.price)}$</b>\n"
                f"📆 Подписка до: <b>{end_date}</b>\n\n"
                "🔗 Переводите на USDT-TRC20:\n"
                "<code>TBLsYqEDqApVkXsizmcF5ivGdi8r2dgm3g</code>\n\n"
                "☝🏽 Жми на кошелек и он автоматически скопируется.\n\n"
                "💳 Как только оплатишь — отправляй хеш транзакции ответным сообщением, и подписка активируется автоматически.\n\n"
                "🆘 По всем вопросам — @glavsot"
            )
            print (f"Item type = {item.type}")
            # Путь к изображению в зависимости от подписки
            photo_path = "image/payment.png"  # Можно настроить пути для разных подписок

            # Выбираем клавиатуру в зависимости от типа подписки
            if item.type == SubscriptionType.Base:
                reply_markup = three_months_keyboard
            elif item.type == SubscriptionType.Whales_club:
                reply_markup = trial_keyboard
            else:
                reply_markup = None  # Если тип не определён, клавиатура не добавляется

            await callback_query.message.answer_photo(
                photo=FSInputFile(photo_path),
                caption=text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    await callback_query.answer()

# Функция для активации подписки (вместо этой функции можно добавить вашу логику активации)
async def activate_subscription(user_id, item_id):
    async with async_session() as session:
        user_subscription = UserSubscription(
            user_id=user_id,
            item_id=item_id,
            start_date=datetime.now(),
            end_date=None,  # Здесь можно добавить логику для расчета даты окончания
            status="active",
            transaction_hash="Транзакционный хеш"  # Можно хранить хеш транзакции в базе
        )
        session.add(user_subscription)
        await session.commit()

async def check_and_expire_subscriptions():
    async with async_session() as session:
        # Получаем все активные подписки
        active_subscriptions = await session.execute(
            select(UserSubscription).where(UserSubscription.status == "active")
        )
        active_subscriptions = active_subscriptions.scalars().all()

        for subscription in active_subscriptions:
            # Если дата окончания подписки не пустая и она прошла
            if subscription.end_date and subscription.end_date < datetime.now():
                # Обновляем статус подписки на "inactive"
                subscription.status = "inactive"
                await session.commit()

                # Отправляем уведомление пользователю о завершении подписки
                user = await session.scalar(select(User).where(User.id == subscription.user_id))
                if user:
                    # Отправляем сообщение пользователю о завершении подписки
                    await send_subscription_expiration_message(user)
                print(f"Подписка пользователя {user.id} на {subscription.item.name} завершена.")
                
async def send_subscription_expiration_message(user: User):
    # Тут можно настроить любое сообщение пользователю по завершению подписки
    await user.send_message("Ваша подписка завершилась. Если хотите продолжить, оформите новую подписку.")
         
        
@router.message(lambda m: m.text and len(m.text.strip()) == 64 and all(c in "0123456789abcdefABCDEF" for c in m.text.strip()))
async def handle_transaction(message: Message, state: FSMContext):
    user_data = await state.get_data()
    item_id = user_data.get("selected_item")

    if not item_id:
        await message.answer("❌ Ошибка! Вы не выбирали подписку перед отправкой транзакции.")
        return

    tx_hash = message.text.strip().replace("Транзакция:", "").strip()
    if len(tx_hash) != 64:
        await message.answer("❌ Ошибка! Неверный формат хеша транзакции.")
        return

    # Проверяем, используется ли хеш транзакции другим пользователем
    async with async_session() as session:
        existing_subscription = await session.scalar(
            select(UserSubscription)
            .where(UserSubscription.transaction_hash == tx_hash)
        )
        if existing_subscription:
            await message.answer("❌ Ошибка! Этот хеш транзакции уже используется другим пользователем.")
            return

    to_address, amount = get_tron_transaction(tx_hash)

    if to_address == "TBLsYqEDqApVkXsizmcF5ivGdi8r2dgm3g" and amount != "Не найдено":
        async with async_session() as session:
            item = await session.scalar(select(Item).where(Item.id == item_id))
            
            if item and float(amount) == item.price:
                end_date = None
                if item.duration != SubscriptionDuration.forever:
                    duration_map = {
                        SubscriptionDuration.one_month: timedelta(days=30),
                        SubscriptionDuration.three_months: timedelta(days=90),
                        SubscriptionDuration.six_months: timedelta(days=180),
                        SubscriptionDuration.one_year: timedelta(days=365)
                    }
                    end_date = datetime.now() + duration_map[item.duration]

                user_subscription = UserSubscription(
                    user_id=message.from_user.id,
                    item_id=item.id,
                    start_date=datetime.now(),
                    end_date=end_date,
                    status="active",
                    transaction_hash=tx_hash
                )

                session.add(user_subscription)
                await session.commit()

                await message.answer(f"✅ Подписка на {item.name} успешно активирована! Добро пожаловать!")
                await state.clear()  # Сбрасываем состояние после успешной покупки
                return

        await message.answer("❌ Ошибка! Неверная сумма перевода.")
    else:
        await message.answer("❌ Ошибка! Неверный адрес получателя или сумма.")



    
        
@router.callback_query(lambda c: c.data == "cancel_subscription_base")
async def cancel_subscription(callback_query: CallbackQuery):
 
    
    caption_text = (
        "<b>РАЗДАЮ АБСОЛЮТНО ВСЕ ПРИВАТКИ ЗА <s>150.000$</s> 39$😱</b>\n\n"
        "Кратко о том, что внутри:\n"
        "<b>• 50+ ПРИВАТОК:</b> доступ ко всем эксклюзивным материалам общей стоимостью 150.000$+ в год\n"
        "<b>• БАЗА ОБУЧЕНИЙ:</b> более 30 курсов по крипте и инвестициям\n"
        "(всегда пополняю ассортимент)\n"
        "<b>• ПОДСВЕЧЕННЫЕ ИДЕИ:</b> мой авторский канал с отборными сделками и инсайдами (личная статистика более +427% / год)\n"
        "<b>• АЛГОТРЕЙДИНГ:</b> возможность делать гарантированные +140% годовых на абсолютном пассиве\n"
        "<b>• ЧАТ КОММЬЮНИТИ:</b> общение, нетворкинг, взаимопомощь и дайджесты по всем приваткам\n"
        "<b>• МЕМКОИНЫ НА х1000:</b> хорошая возможность быстро раскачать свой небольшой депозит\n\n"
        "🎁 Общий созвон на тему стратегии заработка в рынке, которая принесла мне более 393.000$ за 2024 год!\n\n"
        "Подробная презентация в отдельном канале 👉🏽 <a href='https://t.me/clubkitov'><b>ТЫК</b></a>\n\n"
        "<b>💵 СТОИМОСТЬ ДОСТУПА:</b>\n\n"
        "1 месяца — <b>39$</b>\n"
        "3 месяца — <b>99$</b>\n"
        "6 месяцев — <b>179$</b>\n"
        "12 месяцев — <b>349$</b>\n"
        "Навсегда — <b>999$</b>\n\n"
        "Итог: делаешь всё по моей инструкции – зарабатываешь\nот 1000$ за 30 дней. ЖМИ 👇🏽"
    )

    
    # Отправка фото с новым текстом и клавиатурой
    await callback_query.message.answer_photo(
        photo=FSInputFile('image/collage/collage.jpg'),
        caption=caption_text,
        reply_markup=kb.private_by_shef
    )

    # Подтверждаем обработку нажатия кнопки
    await callback_query.answer()

    
#  Обработчик для кнопки "trial_by_shef"
@router.callback_query(lambda c: c.data == "trial_by_shef")
async def send_subscription_message(callback_query: CallbackQuery):
 
    # Вызываем общую функцию для отправки сообщения
    await send_clubkitov_message(callback_query)


async def process_trial_subscription(callback_query: CallbackQuery, duration: SubscriptionDuration, days: int):
    async with async_session() as session:
        item = await session.scalar(
            select(Item).where(
                Item.duration == duration,
                Item.category_id == 2
            )
        )

        if item:
            end_date = (datetime.now() + timedelta(days=days)).strftime('%d.%m.%y')
            text = (
                "💸 | Информация о покупке\n\n"
                f"📌 Продукт: <b>{item.name}</b>\n"
                f"💰 К оплате: <b>{int(item.price)}$</b>\n"
                f"📆 Подписка до: <b>{end_date}</b>\n\n"
                "🔗 Переводите на USDT-TRC20:\n"
                "<code>TBLsYqEDqApVkXsizmcF5ivGdi8r2dgm3g</code>\n\n"
                "☝🏽 Жми на кошелек и он автоматически скопируется.\n\n"
                "💳 Как только оплатишь — отправляй хеш транзакции ответным сообщением, и подписка активируется автоматически.\n\n"
                "🆘 По всем вопросам — @glavsot"
            )

            photo_path = "image/payment.png"
            await callback_query.message.answer_photo(
                photo=FSInputFile(photo_path),
                caption=text,
                parse_mode="HTML",
                reply_markup=trial_keyboard
            )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "whales_three_month")
async def buy_trial_month(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=5)
    await handle_subscription(callback_query, item_id=5)

@router.callback_query(lambda c: c.data == "whales_six_month")
async def buy_trial_quarter(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=6)
    await handle_subscription(callback_query, item_id=6)

@router.callback_query(lambda c: c.data == "whales_one_year")
async def buy_trial_half_year(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=7)
    await handle_subscription(callback_query, item_id=7)

@router.callback_query(lambda c: c.data == "whales_forever")
async def buy_trial_half_year(callback_query: CallbackQuery, state: FSMContext):
 
    await state.update_data(selected_item=8)
    await handle_subscription(callback_query, item_id=8)
    
    
    
    # Обработчик кнопки "trial_by_shef"
@router.callback_query(lambda c: c.data == "cancel_subscription_trial")
async def send_subscription_message(callback_query: CallbackQuery):
 
    text = (
        "РАЗДАЮ АБСОЛЮТНО ВСЕ СКЛАДЧИНЫ ЗА 100.000$ 60$😱\n\n"
        "Кратко, что внутри:\n"
        "• обучение крипте с нуля\n"
        "• подробная инструкция как окупить пробник в 20 раз\n"
        "• доступ ко всем приваткам стоимостью 150.000$ в год\n"
        "• отдельный чат с подсвеченными идеями из всех приваток и живыми результатами\n"
        "• розыгрыш 1000 USDT среди самых активных участников\n\n"
        "🎁 Общий созвон на тему стратегии заработка в рынке, которая принесла мне более 293.000$ за 2023 год!\n\n"
        f"Итог: делаешь всё по моей инструкции – зарабатываешь {hlink('1000$ за 30 дней доступа.', 'https://teletype.in/@deskladchina/14days')}\n\n"
        "Это убийственное предложение, используй его прямо сейчас:"
    )

    # Отправляем исходное сообщение с фото и клавиатурой
    await callback_query.message.answer_photo(
        photo=types.FSInputFile('image/whale.png'),  # Укажите путь к изображению
        caption=text,
        parse_mode="HTML",  # Указываем, что текст содержит HTML-разметку
        reply_markup=subscription_trial_keyboard
    )

    await callback_query.answer()
    



@router.callback_query(lambda c: c.data == "contacts")
async def show_contacts(callback_query: CallbackQuery):
 
    caption_text = (
        "💬 × Ниже находятся все ключевые контакты моей команды. Пишите в любое \nвремя суток — велком ↓\n\n"
        f"{hlink('<b>Главком</b>', 'https://t.me/glavcom')} — по важным вопросам: продуктовая консультация, инвест совет, мнение на актуальную тему.\n\n"
        f"{hlink('<b>Советник</b>', 'https://t.me/glavsot')} — по всем техническим вопросам: бот, пересыл, наши платные продукты, вопросы по торговле / биржам / сделкам."
    )

    # Создаем клавиатуру с кнопкой "Назад"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
        ]
    )

    # Отправляем фото с текстом
    await callback_query.message.answer_photo(
        photo=types.FSInputFile('image/contacts.png'),  # Укажите путь к изображению
        caption=caption_text,
        reply_markup=keyboard,  # Добавляем клавиатуру
        parse_mode="HTML"
    )
    await callback_query.answer()


async def check_subscription_status(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(
                Item.name, 
                Item.category_id,  # Добавляем выбор категории
                UserSubscription.start_date, 
                UserSubscription.end_date, 
                UserSubscription.status
            )
            .join(Item, Item.id == UserSubscription.item_id)
            .where(UserSubscription.user_id == user_id)
        )
        subscriptions = result.fetchall()

        active_subscriptions = []

        for subscription in subscriptions:
            name, category_id, start_date, end_date, status = subscription
            # Проверяем, активна ли подписка
            if end_date and end_date < datetime.now():
                await session.execute(
                    update(UserSubscription)
                    .where(UserSubscription.user_id == user_id, UserSubscription.item_id == subscription.item_id)
                    .values(status="inactive")
                )
                await session.commit()
            else:
                active_subscriptions.append(subscription)

        return active_subscriptions  # Возвращаем подписки с категориями

# Функция для группировки кнопок по два
def chunked(lst, n):
    """Разделяет список на части по n элементов."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]

# Функция для получения списка каналов по категории
async def get_channels_by_category(session, category, has_whales_club):
    query = select(TelegramChannel.name).where(TelegramChannel.category == category)
    
    if not has_whales_club:
        query = query.where(TelegramChannel.type_sub != "Whales_club_only")

    result = await session.execute(query)
    return result.scalars().all()

# Функция для получения категорий (с фильтром)
async def get_filtered_categories(session, exclude_categories):
    query = select(distinct(TelegramChannel.category)).where(
        TelegramChannel.category.isnot(None),
        TelegramChannel.category.notin_(exclude_categories)
    )
    result = await session.execute(query)
    return result.scalars().all()

@router.callback_query(lambda c: c.data == "my_access")
async def show_my_access(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user_id = callback_query.from_user.id

    # Получаем никнейм пользователя
    user_name = callback_query.from_user.full_name

    # Формируем текст с приветствием
    text = (
        f"<b>🕹️ × Личный кабинет, {user_name}</b>\n\n"
        "Добро пожаловать в личный\nкабинет, ниже находятся\nвсе твои доступы. "
        "Если\nбудут какие-либо вопросы\nпиши моему "
        "<a href='https://t.me/glavsot'><b>советнику</b></a>.\n\n"
        "<b>АКТУАЛЬНЫЕ ПОДПИСКИ:</b>\n\n"
    )

    async with async_session() as session:
        subscriptions = await check_subscription_status(user_id)

        if subscriptions:
            for name, category_id, start_date, end_date, status in subscriptions:
                # Определяем отображаемое название в зависимости от категории
                if category_id == 1:
                    display_name = "База"
                elif category_id == 2:
                    display_name = "Клуб Китов"
                else:
                    display_name = name  # Оставляем оригинальное название, если категория неизвестна

                # Вычисляем оставшиеся дни подписки
                if end_date:
                    remaining_days = (end_date - datetime.now()).days
                    if remaining_days > 0:
                        text += f"— {display_name}: {remaining_days} дней\n"
                    else:
                        text += f"— {display_name}: Подписка истекла\n"
                else:
                    text += f"— {display_name}: Навсегда\n"

    # Добавляем текст с инструкцией
    text += (
        "\nДля продления подписки\nжми на гиперссылку выше, или\nпиши мне напрямую: <b>@glavcom.</b>\n\n"
        "<i>Для получения доступа к товару жми нужную тебе кнопку ниже.</i>"
    )

    # Путь к изображению
    photo_path = "image/cabinet.png"

    # Отправляем фото с текстом и клавиатурой
    await callback_query.message.answer_photo(
        photo=FSInputFile(photo_path),
        caption=text,
        parse_mode="HTML",
        reply_markup=personal_buttons_keyboard
    )

    await callback_query.answer()


async def check_for_base_subscription(user_id: int, session) -> bool:
    # Проверяем, есть ли у пользователя подписка с item_id 1, 2, 3 или 4
    result = await session.execute(
        select(UserSubscription.item_id)
        .where(UserSubscription.user_id == user_id)
    )
    subscriptions = result.fetchall()

    # Проверяем наличие подписки с item_id 1, 2, 3 или 4
    for subscription in subscriptions:
        if subscription[0] in [1, 2, 3, 4]:
            return True
    return False


from aiogram.types import FSInputFile  # Импортируем FSInputFile для работы с локальными файлами

@router.callback_query(lambda c: c.data == "channels")
async def show_main_menu(callback_query: CallbackQuery):
    await callback_query.message.delete()  # Удаляем предыдущее сообщение
    user_id = callback_query.from_user.id
    subscriptions = await check_subscription_status(user_id)

    # Проверка подписки пользователя
    if not subscriptions:
        await callback_query.message.answer("❌ У вас нет активных подписок. Приобретите доступ в магазине.")
        await callback_query.answer()
        return

    # Проверка базовой подписки
    async with async_session() as session:
        has_base_subscription = await check_for_base_subscription(user_id, session)

    # Создаем клавиатуру
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Все каналы", callback_data="all_channels")]
        ]
    )

    # Добавляем кнопку для Discord приваток, если нет базовой подписки
    if not has_base_subscription:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text="Discord приватки", callback_data="category_Discord приватки")])

    # Добавляем кнопку "Вернуться"
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="Вернуться", callback_data="my_access")])

    # Отправляем изображение
    await callback_query.message.answer_photo(
        photo=FSInputFile("image/clubs.png"),  # Укажите путь к локальной картинке
        caption="Выберите раздел:",  # Подпись к изображению
        reply_markup=keyboard  # Прикрепляем клавиатуру
    )

    await callback_query.answer()  # Подтверждаем обработку callback


async def get_channel_invite_link(session, channel_name: str):
    # Ищем канал по имени в таблице TelegramChannels
    result = await session.execute(
        select(TelegramChannel.invite_link).filter(TelegramChannel.name == channel_name)
    )
    channel = result.scalars().first()  # Получаем первую ссылку, если она есть
    return channel  # Если канала нет, вернется None

from aiogram.types import FSInputFile  # Импортируем FSInputFile для работы с локальными файлами

@router.callback_query(lambda c: c.data == "all_channels")
async def show_all_categories(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user_id = callback_query.from_user.id
    subscriptions = await check_subscription_status(user_id)

    if not subscriptions:
        await callback_query.message.answer("❌ У вас нет активных подписок. Приобретите доступ в магазине.")
        await callback_query.answer()
        return

    async with async_session() as session:
        categories = await get_filtered_categories(session, ["Discord приватки", "Курсы"])

    if not categories:
        await callback_query.message.answer("❌ Нет доступных категорий.")
        await callback_query.answer()
        return

    buttons = [
        InlineKeyboardButton(text=category, callback_data=f"category_{category}") for category in categories
    ]
    chunked_buttons = chunked(buttons, 2)
    chunked_buttons.append([InlineKeyboardButton(text="Назад", callback_data="channels")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=chunked_buttons)
    text = "Выберите категорию:"

    await callback_query.message.answer(text, reply_markup=keyboard)
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("category_"))
async def show_channels_by_category(callback_query: CallbackQuery):
    await callback_query.message.delete()
    category_name = callback_query.data.replace("category_", "")

    async with async_session() as session:
        result = await session.execute(
            select(TelegramChannel.name, TelegramChannel.invite_link, TelegramChannel.description, TelegramChannel.image_url)
            .where(TelegramChannel.category == category_name)
        )
        channels = result.fetchall()

    if not channels:
        await callback_query.message.answer("❌ В этой категории нет каналов.")
        await callback_query.answer()
        return

    # Берём описание и картинку только из первого канала категории
    description = channels[0][2] if channels[0][2] else "Описание отсутствует."
    image_url = channels[0][3]

    # Создаём кнопки для перехода в каналы
    buttons = [
        InlineKeyboardButton(text=name, url=invite_link) for name, invite_link, _, _ in channels
    ]

    # Формируем кнопки в столбцы
    chunked_buttons = chunked(buttons, 2)  # Разбиваем на группы по 2 кнопки

    # Навигационные кнопки
    current_index = channels.index(channels[0])
    prev_channel = channels[current_index - 1] if current_index > 0 else channels[-1]
    next_channel = channels[(current_index + 1) % len(channels)]

    navigation_buttons = [
        InlineKeyboardButton(text="⬅️", callback_data=f"category_{category_name}_{prev_channel[0]}"),
        InlineKeyboardButton(text="➡️", callback_data=f"category_{category_name}_{next_channel[0]}")
    ]

    chunked_buttons.append(navigation_buttons)
    chunked_buttons.append([InlineKeyboardButton(text="Назад", callback_data="channels")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=chunked_buttons)

    text = f"<b>{category_name}</b>\n\n{description}"

    # Отправляем фото с описанием и кнопками
    if image_url:
        await callback_query.message.answer_photo(
            photo=image_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        await callback_query.message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    await callback_query.answer()




    
# Обработчик для "Discord приватки"
@router.callback_query(lambda c: c.data == "category_Discord приватки")
async def show_discord_private(callback_query: CallbackQuery):
    await callback_query.message.delete()
    category = "Discord приватки"
    user_id = callback_query.from_user.id
    subscriptions = await check_subscription_status(user_id)
    user_types = {sub[0] for sub in subscriptions}
    has_whales_club = any("Whales club" in sub_type for sub_type in user_types)

    async with async_session() as session:
        # Получаем каналы в категории
        channels = await get_channels_by_category(session, category, has_whales_club)

    # Формируем текст сообщения
    text = f"📂 Категория: {category}\n\nВыберите канал."

    # Создаем кнопки для всех каналов
    buttons = [InlineKeyboardButton(text=channel, callback_data=f"channel_{channel}") for channel in channels]
    chunked_buttons = chunked(buttons, 2)
    
    # Кнопка "Назад"
    chunked_buttons.append([InlineKeyboardButton(text="Назад", callback_data="channels")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=chunked_buttons)

    # Отправляем сообщение с клавиатурой для выбора канала
    await callback_query.message.answer(text, reply_markup=keyboard)
    await callback_query.answer()


async def get_channel_info(session, channel_name):
    # Запрос к базе данных для получения информации о канале
    result = await session.execute(
        select(TelegramChannel.description, TelegramChannel.image_url, TelegramChannel.invite_link)
        .where(TelegramChannel.name == channel_name)
    )
    channel_info = result.first()
    if channel_info:
        return {
            "description": channel_info.description,
            "image_url": channel_info.image_url,
            "invite_link": channel_info.invite_link
        }
    return None

@router.callback_query(lambda c: c.data.startswith("channel_"))
async def show_channel_info(callback_query: CallbackQuery):
    await callback_query.message.delete()
    channel_name = callback_query.data.replace("channel_", "")
    user_id = callback_query.from_user.id
    subscriptions = await check_subscription_status(user_id)
    user_types = {sub[0] for sub in subscriptions}
    has_whales_club = any("Whales club" in sub_type for sub_type in user_types)

    async with async_session() as session:
        # Получаем все каналы для пользователя в категориях "Discord приватки" и "Курсы"
        discord_channels = await get_channels_by_category(session, "Discord приватки", has_whales_club)
        course_channels = await get_channels_by_category(session, "Курсы", has_whales_club)
        
        # Определяем, к какой категории принадлежит текущий канал
        if channel_name in discord_channels:
            category = "Discord приватки"
            all_channels = discord_channels
        elif channel_name in course_channels:
            category = "Курсы"
            all_channels = course_channels
        else:
            await callback_query.answer("Канал не найден.", show_alert=True)
            return

        # Получаем информацию о канале (описание и URL изображения)
        channel_info = await get_channel_info(session, channel_name)
        if not channel_info:
            await callback_query.answer("Информация о канале не найдена.", show_alert=True)
            return

        description = channel_info.get("description")
        image_url = channel_info.get("image_url")
        invite_link = channel_info.get("invite_link")

        if not invite_link:
            await callback_query.answer("Ссылка на канал не найдена.", show_alert=True)
            return

    # Находим текущий канал в списке
    current_index = all_channels.index(channel_name)
    prev_channel = all_channels[current_index - 1] if current_index > 0 else all_channels[-1]
    next_channel = all_channels[(current_index + 1) % len(all_channels)]

    # Формируем текстовое сообщение с названием канала, описанием и ссылкой
    text = f"📢 Канал: {channel_name}\n\n{description}\n\nНажмите стрелки для навигации.\n\n"

    # Создаем кнопку с названием канала и ссылкой (кнопка будет большой)
    channel_button = InlineKeyboardButton(text=channel_name, url=invite_link)

    # Кнопки навигации (нормального размера)
    navigation_buttons = [
        InlineKeyboardButton(text="⬅️", callback_data=f"channel_{prev_channel}"),
        InlineKeyboardButton(text="➡️", callback_data=f"channel_{next_channel}")
    ]
    
    # Кнопка "Назад" (большая, внизу)
    back_button = InlineKeyboardButton(text="Назад", callback_data=f"category_{category}")

    # Формируем клавиатуру
    chunked_buttons = chunked(navigation_buttons, 2)
    
    # Добавляем большую кнопку для канала в центр и большую кнопку "Назад" внизу
    chunked_buttons.append([channel_button])  # Добавляем кнопку с ссылкой в центр
    chunked_buttons.append([back_button])  # Добавляем кнопку "Назад" внизу

    # Создаем клавиатуру с опцией resize для больших кнопок
    keyboard = InlineKeyboardMarkup(inline_keyboard=chunked_buttons, resize_keyboard=True)

    # Отправляем фото с описанием и кнопками навигации
    if image_url:
        try:
            await callback_query.message.answer_photo(
                photo=image_url,  # Передаем URL изображения
                caption=text,  # Описание канала
                reply_markup=keyboard,  # Клавиатура с кнопками
                parse_mode="HTML"  # Указываем, что текст содержит HTML-разметку
            )
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            await callback_query.message.answer(
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
    else:
        await callback_query.message.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    await callback_query.answer()
    
    
@router.callback_query(lambda c: c.data == "category_Курсы")
async def show_courses(callback_query: CallbackQuery):
    # Удаляем предыдущее сообщение
    await callback_query.message.delete()
    category = "Курсы"
    user_id = callback_query.from_user.id
    subscriptions = await check_subscription_status(user_id)

    # Проверяем, есть ли у пользователя подписка на "Whales club"
    user_types = {sub[0] for sub in subscriptions}
    has_whales_club = any("Whales club" in sub_type for sub_type in user_types)

    if not has_whales_club:
        # Если нет подписки на Whales club, отправляем сообщение
        await callback_query.message.answer("❌ У вас нет подписки на Whales club. Приобретите доступ в магазине.")
        await callback_query.answer()
        return

    async with async_session() as session:
        # Получаем каналы в категории "Курсы" (с учетом подписки на Whales club)
        channels = await get_channels_by_category(session, category, has_whales_club)

    # Формируем текст сообщения
        # Формируем текстовое сообщение
    text = (
        "🏴‍☠️ × В этом разделе ты найдешь ссылки на все доступные тебе курсы. Напомню — у телеги стоит спам ограничение в 5 вступлений каждые 5-10 минут.\n\n"
        "• <b>Обязательно к изучению</b> — лучшие курсы по нашему мнению, которые нужно пройти в обязательном порядке (по сути в остальное можно не заходить).\n\n"
        "• <b>Все курсы</b> — список абсолютно всех доступных обучений."
    )


    # Создаем кнопки для всех каналов
    buttons = [InlineKeyboardButton(text=channel, callback_data=f"channel_{channel}") for channel in channels]
    chunked_buttons = chunked(buttons, 2)
    
    # Кнопка "Назад"
    chunked_buttons.append([InlineKeyboardButton(text="Назад", callback_data="my_access")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=chunked_buttons)

    # Путь к изображению
    photo_path = "image/courses.png"  # Укажите путь к вашему изображению

    # Отправляем фото с текстом и клавиатурой
    await callback_query.message.answer_photo(
        photo=FSInputFile(photo_path),  # Используем FSInputFile для загрузки локального файла
        caption=text,  # Текст сообщения
        reply_markup=keyboard  # Клавиатура
    )

    await callback_query.answer()

