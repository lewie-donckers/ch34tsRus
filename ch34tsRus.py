from ..bot_control import Move


class ch34tsRus:

    def __init__(self):
        pass

    def get_name(self):
        return "Hein Won't Let Me Cheat"

    def get_contributor(self):
        return "Lewie"

    def determine_next_move(self, grid, enemies, game_info):
        grid.fill(self.id)
        return Move.STAY
