class ClubValidationError(Exception):
    def __init__(self, club_id, message = None):
        self.club_id = club_id
        if message is None:
            message = f'Клуб с id = {self.club_id} не найден! Введите верный id!'
        super().__init__(message)


class PlayerValidationError(Exception):
    def __init__(self, player_id, message = None):
        self.player_id = player_id
        if message is None:
            message = f"Футболист с id = {self.player_id} не найден! Введите верный id!"
        super().__init__(message)


class NothingExists(Exception):
    def __init__(self, object_id, message = None):
        self.object_id = object_id
        if message is None:
            message = f"Футболиста или клуба с id = {self.object_id} не существует! Введите верный id!"
        super().__init__(message)
