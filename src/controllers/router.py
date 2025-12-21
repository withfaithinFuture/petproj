from fastapi import APIRouter, Depends
from typing import Dict, Annotated
from src.services.repositories.repositories import ClubFootballersRepository
from src.services.schemas.schemas import ClubSchema

router = APIRouter()


@router.get('/healthcheck')
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@router.post('/Клубы')
async def add_club(club: ClubSchema):
    club_id = await ClubFootballersRepository.add_club(club)
    return {'Club_id': club_id, 'status': True}