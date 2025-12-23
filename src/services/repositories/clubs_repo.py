from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from services.exceptions import NothingExists
from src.services.repositories.ready_info import ReadyInfoForAddRepo
from src.services.schemas.schemas import PlayerSchemaUpdate
from src.services.schemas.schemas import ClubSchemaUpdate
from src.models.football_players import Player
from src.services.schemas.schemas import ClubSchema
from src.models.clubs import Club



class ClubFootballersRepository:
    @classmethod
    async def add_club(cls, club_data: ClubSchema, db_session: AsyncSession):
        club, players = ReadyInfoForAddRepo.get_club_and_players(club_data)
        club.players = players

        db_session.add(club)
        db_session.add_all(players)
        await db_session.flush()
        await db_session.refresh(club)

        return club_data


    @classmethod
    async def get_clubs_info(cls, db_session: AsyncSession):
        result = await db_session.execute(select(Club).options(selectinload(Club.players))) #сразу загрузка и игроков
        clubs_models = result.scalars().all()
        clubs_schemas = [ClubSchema.model_validate(club) for club in clubs_models]
        return clubs_schemas


    @classmethod
    async def update_clubs_info(cls, update_sch: ClubSchemaUpdate, db_session: AsyncSession):
        update_sch_dict = update_sch.model_dump(exclude_none=True)
        query = select(Club).where(Club.id == update_sch.id).options(selectinload(Club.players))
        result = await db_session.execute(query)
        existing_club = result.scalar_one_or_none()

        for key, value in update_sch_dict.items():
            if hasattr(existing_club, key):
                setattr(existing_club, key, value)

        await db_session.flush()
        await db_session.refresh(existing_club)

        return ClubSchema.model_validate(existing_club)


    @classmethod
    async def update_players_info(cls, update_player_sch: PlayerSchemaUpdate, db_session: AsyncSession):
        update_sch_dict = update_player_sch.model_dump(exclude_none=True)
        query = select(Player).where(Player.id == update_player_sch.id)
        result_player = await db_session.execute(query)
        existing_player = result_player.scalar_one_or_none()

        for key, value in update_sch_dict.items():
            if hasattr(existing_player, key):
                setattr(existing_player, key, value)

        return update_player_sch


    @classmethod
    async def delete_club_or_player(cls, delete_id, db_session: AsyncSession):
        query1 = select(Club).where(Club.id == delete_id)
        query2 = select(Player).where(Player.id == delete_id)
        result1 = await db_session.execute(query1)
        result2 = await db_session.execute(query2)
        existing_club, existing_player = result1.scalar_one_or_none(), result2.scalar_one_or_none()

        if existing_club is None and existing_player is None:
            raise NothingExists(delete_id)

        elif existing_club:
            await db_session.delete(existing_club)
            return existing_club

        else:
            await db_session.delete(existing_player)
            return existing_player