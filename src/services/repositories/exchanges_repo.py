from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.exchange_owners import Owner
from src.models.exchanges import Exchange
from src.services.schemas.schemas import ExchangeSchema


class ExchangesOwnersRepository:
    @classmethod
    async def add_exchange(cls, exchange_data: ExchangeSchema, db_session: AsyncSession):
        owner_data_dict, exchange_data_dict = exchange_data.owner.model_dump(), exchange_data.model_dump(exclude='owner')
        owner, exchange = Owner(**owner_data_dict), Exchange(**exchange_data_dict)
        exchange.owner = owner

        db_session.add(owner)
        db_session.add(exchange)
        await db_session.flush()
        await db_session.refresh(exchange)

        return exchange


    @classmethod
    async def get_exchanges_info(cls, db_session: AsyncSession):
        query = select(Exchange).options(selectinload(Exchange.owner))
        result = await db_session.execute(query)
        result_models = result.scalars().all()
        exchanges = [ExchangeSchema.model_validate(exchange) for exchange in result_models]
        return exchanges


    @classmethod
    async def update_exchange_info(cls, update_info: ExchangeUpdateSchema, db_session: AsyncSession):
        pass