from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.football_players import Player
from src.services.schemas.schemas import ClubSchema
from src.models.clubs import Club


class ClubFootballersRepository:
    @classmethod
    async def add_club(cls, club_data: ClubSchema, db_session: AsyncSession):
        async with db_session as session:
            club_data_dict = club_data.model_dump(exclude='players')
            new_club = Club(**club_data_dict)
            session.add(new_club)

            for player in club_data.players:
                player_data_dict = player.model_dump()
                new_player = Player(**player_data_dict)
                session.add(new_player)

                new_club.players.append(new_player)

            await session.commit()
            return new_club.id

    @classmethod
    async def get_clubs_info(cls, db_session: AsyncSession):
        async with db_session as session:
            result = await session.execute(select(Club).options(selectinload(Club.players))) #сразу загрузка и игроков
            clubs_models = result.scalars().all()
            clubs_schemas = [ClubSchema.model_validate(club) for club in clubs_models]
            return clubs_schemas


    # @classmethod
    # async def update_clubs_info(cls, club_name: str, db_session: AsyncSession):
    #     return club_name
