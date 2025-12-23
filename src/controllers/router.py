from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from src.services.exceptions import NothingExists
from src.services.repositories.exchanges_repo import ExchangesOwnersRepository
from src.services.dependencies import validate_exist_player, ClubValidationError, PlayerValidationError
from src.services.dependencies import validate_exist_club
from src.services.schemas.schemas import ClubSchemaUpdate, PlayerSchemaUpdate, ExchangeSchema
from src.services.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.repositories.clubs_repo import ClubFootballersRepository
from src.services.schemas.schemas import ClubSchema


router = APIRouter()

@router.get('/healthcheck')
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@router.post('/Клубы/Добавление клуба с игроками', tags=['Действия с футбольным клубами']) #через depends
async def add_club(club: ClubSchema, db_session: AsyncSession = Depends(get_session)):
    club = await ClubFootballersRepository.add_club(club, db_session)
    return {'Club': club, 'HTTP status': 201}

@router.get('/Клубы/Получение', tags=['Действия с футбольным клубами'])
async def get_clubs(db_session: AsyncSession = Depends(get_session)):
    clubs = await ClubFootballersRepository.get_clubs_info(db_session)
    return {"Clubs": clubs, 'HTTP status': 200}

@router.patch('/Клубы/Обновление клубов', tags=['Действия с футбольным клубами'])
async def update_clubs(club_update: ClubSchemaUpdate, db_session: AsyncSession = Depends(get_session)):
    try:
        await validate_exist_club(club_update, db_session)
        updated_club = await ClubFootballersRepository.update_clubs_info(club_update, db_session)
        return {'New club info': updated_club, 'HTTP status': 200}

    except ClubValidationError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})

@router.patch('/Клубы/Обновление игроков', tags=['Действия с футбольным клубами'])
async def update_players(player_update: PlayerSchemaUpdate, db_session: AsyncSession = Depends(get_session)):
    try:
        await validate_exist_player(player_update, db_session)
        updated_player = await ClubFootballersRepository.update_players_info(player_update, db_session)
        return {'New player info': updated_player, 'HTTP status': 200}

    except PlayerValidationError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})


@router.post('/Клубы/Удаление игрока или клуба', tags=['Действия с футбольным клубами'])
async def delete_by_id(delete_id, db_session: AsyncSession = Depends(get_session)):
    try:
        deleted_object = await ClubFootballersRepository.delete_club_or_player(delete_id, db_session)
        return {'Deleted object': deleted_object, 'HTTP status': 200}

    except NothingExists as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})


@router.post('/Биржа/Добавление биржи', tags=['Действия с биржами'])
async def add_exchange(exchange_data: ExchangeSchema, db_session: AsyncSession = Depends(get_session)):
    new_exchange = await ExchangesOwnersRepository.add_exchange(exchange_data, db_session)
    return new_exchange

@router.get('/Биржа/Добавление биржи', tags=['Действия с биржами'])
async def get_exchanges(db_session: AsyncSession = Depends(get_session)):
    exchanges = await ExchangesOwnersRepository.get_exchanges_info(db_session)
    return exchanges

@router.patch('/Биржа/Добавление биржи', tags=['Действия с биржами'])
async def update_exchange(update_data: ExchangeUpdateSchema, db_session: AsyncSession = Depends(get_session)):
    pass