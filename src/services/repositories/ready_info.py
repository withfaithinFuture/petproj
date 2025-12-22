from src.models.clubs import Club
from src.models.football_players import Player


class ReadyInfoForAddRepo:
    @staticmethod
    def get_club_and_players(club_data):
        club_data_dict = club_data.model_dump(exclude='players')
        new_club = Club(**club_data_dict)

        players = []
        for player in club_data.players:
            player_data_dict = player.model_dump()
            new_player = Player(**player_data_dict)
            players.append(new_player)

        return new_club, players
