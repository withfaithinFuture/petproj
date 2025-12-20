from sqlalchemy import ForeignKey, Column, Table
from src.services.data_service import Base


joined_table = Table(
    'clubs_and_players', Base.metadata,
    Column('club_id', ForeignKey('clubs.id')),
    Column('player id', ForeignKey('players.id'))
)
