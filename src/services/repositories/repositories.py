from sqlalchemy import select
from src.models.football_players import Player
from src.services.schemas.schemas import ClubSchema
from src.services.db import get_session
from src.models.clubs import Club


class ClubFootballersRepository:
    @classmethod
    async def add_club(cls, Club_data: ClubSchema):
        async with get_session() as session:
            async with session.begin(): #транза для нескольких действий
                club_data_dict = Club_data.model_dump(exclude='players')
                new_club = Club(**club_data_dict)
                session.add(new_club)
                await session.flush()
                await session.refresh(new_club, ['players'])

                for player in Club_data.players:
                    player_data_dict = player.model_dump()
                    new_player = Player(**player_data_dict)

                    check = select(Player).where(player_data_dict["id"] == Player.id)
                    check_result = await session.execute(check)
                    player_exist = check_result.scalar_one_or_none()

                    if player_exist:
                        player_add = player_exist
                    else:
                        session.add(new_player)
                        await session.flush()
                        player_add = new_player

                    new_club.players.append(player_add)


