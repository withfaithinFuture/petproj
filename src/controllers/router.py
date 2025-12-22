from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Dict
from src.services.dependencies import validate_exist_player
from src.services.dependencies import validate_exist_club
from services.schemas.schemas import ClubSchemaUpdate, PlayerSchemaUpdate
from src.services.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.repositories.clubs_repo import ClubFootballersRepository
from src.services.schemas.schemas import ClubSchema


router = APIRouter()

@router.get('/healthcheck')
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@router.post('/Клубы/Добавление', tags=['Действия с футбольным клубами']) #через depends
async def add_club(club: ClubSchema, db_session: AsyncSession = Depends(get_session)):
    club = await ClubFootballersRepository.add_club(club, db_session)
    return {'Club': club, 'Addition status': True}

@router.get('/Клубы/Получение', tags=['Действия с футбольным клубами'])
async def get_clubs(db_session: AsyncSession = Depends(get_session)):
    clubs = await ClubFootballersRepository.get_clubs_info(db_session)
    return clubs

@router.patch('/Клубы/Обновление клубов', tags=['Действия с футбольным клубами'])
async def update_clubs(club_update: ClubSchemaUpdate = Depends(validate_exist_club), db_session: AsyncSession = Depends(get_session)):
    updated_club = await ClubFootballersRepository.update_clubs_info(club_update, db_session)
    return updated_club

@router.patch('/Клубы/Обновление игроков', tags=['Действия с футбольным клубами'])
async def update_players(player_update: PlayerSchemaUpdate = Depends(validate_exist_player), db_session: AsyncSession = Depends(get_session)):
    updated_player = await ClubFootballersRepository.update_players_info(player_update, db_session)
    return updated_player

@router.post('/Клубы/Удаление игрока или клуба', tags=['Действия с футбольным клубами'])
async def delete_by_id(delete_id, db_session: AsyncSession = Depends(get_session)):
    deleted_object = await ClubFootballersRepository.delete_club_or_player(delete_id, db_session)
    return deleted_object
