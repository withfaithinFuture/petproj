from fastapi import APIRouter, Depends
from typing import Dict
from src.services.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.repositories.repositories import ClubFootballersRepository
from src.services.schemas.schemas import ClubSchema


router = APIRouter()

@router.get('/healthcheck')
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@router.post('/Клубы/Добавление', tags=['Действия с футбольным клубами']) #через depends
async def add_club(club: ClubSchema, db_session: AsyncSession = Depends(get_db_session)):
    club_id = await ClubFootballersRepository.add_club(club, db_session)
    return {'Club_id': club_id, 'status': True}

@router.get('/Клубы/Получение', tags=['Действия с футбольным клубами'])
async def get_clubs(db_session: AsyncSession = Depends(get_db_session)):
    clubs = await ClubFootballersRepository.get_clubs_info(db_session)
    return clubs

# @router.post('/Клубы/Обновление', tags=['Действия с футбольным клубами'])
# async def update_clubs(club_name: str, db_session: AsyncSession = Depends(get_db_session)):
#     clubs_name = await ClubFootballersRepository.update_clubs_info(club_name, db_session)
#     return clubs_name