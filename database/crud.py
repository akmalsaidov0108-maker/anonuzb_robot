from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update
from database.models import Base, User
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_or_create_user(telegram_id: int, username: str, full_name: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=telegram_id, username=username, full_name=full_name)
            session.add(user)
            await session.commit()
        return user

async def set_gender(telegram_id: int, gender: str):
    async with async_session() as session:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(gender=gender))
        await session.commit()

async def get_user(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

async def set_searching(telegram_id: int, status: bool):
    async with async_session() as session:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(is_searching=status))
        await session.commit()

async def set_partner(telegram_id: int, partner_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(partner_id=partner_id, is_searching=False))
        await session.commit()

async def get_waiting_user(exclude_id: int, gender_filter=None):
    async with async_session() as session:
        query = select(User).where(User.is_searching == True, User.telegram_id != exclude_id, User.is_banned == False)
        if gender_filter:
            query = query.where(User.gender == gender_filter)
        result = await session.execute(query)
        return result.scalars().first()

async def disconnect_user(telegram_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(partner_id=None, is_searching=False))
        await session.commit()

async def ban_user(telegram_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(is_banned=True))
        await session.commit()

async def get_all_users_count():
    async with async_session() as session:
        result = await session.execute(select(User))
        return len(result.scalars().all())
