from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.exchange_owners import Owner
from src.models.exchanges import Exchange
from src.services.exceptions import ClubValidationError, PlayerValidationError, ExchangeValidateError, \
    OwnerValidateError
from src.models.football_players import Player
from src.models.clubs import Club
from src.services.schemas.schemas import ClubSchemaUpdate, PlayerSchemaUpdate, ExchangeUpdateSchema, \
    ExchangeOwnerUpdateSchema


async def validate_exist_club(data: ClubSchemaUpdate, session: AsyncSession):
    club = data.model_dump()
    club_id = club.get("id")
    query = select(Club).where(Club.id == club_id)
    result = await session.execute(query)
    existing_club = result.scalar_one_or_none()

    if not existing_club:
        raise ClubValidationError(club_id)

    return data


async def validate_exist_player(data: PlayerSchemaUpdate, session: AsyncSession):
    player = data.model_dump()
    player_id = player.get("id")
    query = select(Player).where(Player.id == player_id)
    result = await session.execute(query)
    existing_player = result.scalar_one_or_none()

    if not existing_player:
        raise PlayerValidationError(player_id)

    return data


async def validate_exchange_exist(data: ExchangeUpdateSchema, db_session: AsyncSession):
    update_data = data.model_dump()
    query = select(Exchange).where(update_data['id'] == Exchange.id)
    result = await db_session.execute(query)
    exist_object = result.scalar_one_or_none()

    if exist_object is None:
        raise ExchangeValidateError(update_data['id'])


async def validate_owner_exist(data: ExchangeOwnerUpdateSchema, db_session: AsyncSession):
    data_dict = data.model_dump()
    query = select(Owner).where(data_dict['id'] == Owner.id)
    result = await db_session.execute(query)
    exist_owner = result.scalar_one_or_none()

    if exist_owner is None:
        raise OwnerValidateError(data_dict['id'])

