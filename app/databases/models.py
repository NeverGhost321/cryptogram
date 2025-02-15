import asyncio
from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
import enum
from datetime import datetime, timedelta

# Создаем асинхронный движок для базы данных
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

# Создаем фабрику сессий
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Создаем базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Обновленное перечисление для типов подписок
class SubscriptionType(enum.Enum):
    Base = "Base"  # Подписка "Private" — Base
    Whales_club = "Whales club"  # Пробная подписка — Whales_club
    biohacking = "biohacking"  # Подписка на биохакинг — biohacking

# Перечисление для продолжительности подписок
class SubscriptionDuration(enum.Enum):
    one_month = "1 месяц"
    three_months = "3 месяца"
    six_months = "6 месяцев"
    one_year = "1 год"
    forever = "навсегда"

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  # Используем BigInteger в mapped_column
    username: Mapped[str] = mapped_column(nullable=True)
    
    subscriptions = relationship("UserSubscription", back_populates="user")  # Связь с подписками


# Модель для категорий товаров
class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    
    items = relationship("Item", back_populates="category")

# Модель для товаров (подписок)
class Item(Base):
    __tablename__ = 'items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    type: Mapped[SubscriptionType] = mapped_column(Enum(SubscriptionType))
    duration: Mapped[SubscriptionDuration] = mapped_column(Enum(SubscriptionDuration))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))  # Исправлено: добавлен ForeignKey
    
    category = relationship("Category", back_populates="items")
    user_subscriptions = relationship("UserSubscription", back_populates="item")

class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    transaction_hash: Mapped[str] = mapped_column(String, nullable=True)

    # Добавляем связь с Telegram-каналом
    channel_id: Mapped[int] = mapped_column(ForeignKey('telegram_channels.id'), nullable=True)
    channel = relationship("TelegramChannel", back_populates="subscriptions")
    
    # Добавляем связь с пользователем
    user = relationship("User", back_populates="subscriptions")
    item = relationship("Item", back_populates="user_subscriptions")

# Функция для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class TelegramChannel(Base):
    __tablename__ = 'telegram_channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # Название канала
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  # ID канала в Telegram
    invite_link: Mapped[str] = mapped_column(String, nullable=True)  # Ссылка на приглашение
    category: Mapped[str] = mapped_column(String, nullable=True)  # Категория канала
    type_sub: Mapped[str] = mapped_column(String, nullable=True)  # Тип подписки
    description: Mapped[str] = mapped_column(String(1024), nullable=True)  # Описание канала (максимум 1024 символа)
    image_url: Mapped[str] = mapped_column(String, nullable=True)  # URL-ссылка на изображение канала

    # Связь с подписками
    subscriptions = relationship("UserSubscription", back_populates="channel")