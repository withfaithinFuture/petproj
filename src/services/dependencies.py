from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.football_players import Player
from services.db import get_session
from src.models.clubs import Club
from src.services.schemas.schemas import ClubSchemaUpdate, PlayerSchemaUpdate


async def validate_exist_club(data: ClubSchemaUpdate, session: AsyncSession = Depends(get_session)):
    club = data.model_dump()
    club_id = club.get("id")
    query = select(Club).where(Club.id == club_id)
    result = await session.execute(query)
    existing_club = result.scalar_one_or_none()

    if not existing_club:
        raise HTTPException(status_code=404, detail="Введите id существующего клуба!")

    return data


async def validate_exist_player(data: PlayerSchemaUpdate, session: AsyncSession = Depends(get_session)):
    player = data.model_dump()
    player_id = player.get("id")
    query = select(Player).where(Player.id == player_id)
    result = await session.execute(query)
    existing_player = result.scalar_one_or_none()

    if not existing_player:
        raise HTTPException(status_code=404, detail="Введите id существующего игрока!")

    return data

