class Game:
    def __init__(self, creator, name, nb_max_players, type, map, password = '',  is_running = False):
        self.creator = creator
        self.name = name
        self.nb_max_players = nb_max_players
        self.type = type
        self.map = map
        self.password = password
        self.is_running = is_running
        self.players = []
        self.players.append(creator)