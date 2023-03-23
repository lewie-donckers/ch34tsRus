import collections
import numpy
from ..bot_control import Move

_Enemy = collections.namedtuple('Enemy', ['id', 'position'])


class _Position:
    _vectors = {
        Move.UP: (0, 1),
        Move.DOWN: (0, -1),
        Move.LEFT: (-1, 0),
        Move.RIGHT: (1, 0)
    }

    def __init__(self, *, x, y):
        self.x = x
        self.y = y

    def is_valid(self, grid_size):
        return (self.x >= 0) and (self.y >= 0) and (self.x < grid_size) and (
            self.y < grid_size)

    def step(self, move):
        vector = __class__._vectors.get(move, (0, 0))
        return self.add(vector)

    def add(self, vector):
        return _Position(x=self.x + vector[0], y=self.y + vector[1])

    def vector(self, target):
        return (target.x - self.x, target.y - self.y)

    def distance(self, target):
        vector = self.vector(target)
        return abs(vector[0]) + abs(vector[1])

    def __str__(self):
        return "Position({}, {})".format(self.x, self.y)

    @staticmethod
    def fromNumpy(n):
        return _Position(x=n[0], y=n[1])


def _create_search_vector(distance):
    return {
        Move.UP: [(i, distance - i) for i in range(0, distance)],
        Move.RIGHT: [(i, -distance + i) for i in range(distance, 0, -1)],
        Move.DOWN: [(i, -distance - i) for i in range(0, -distance, -1)],
        Move.LEFT: [(i, distance + i) for i in range(-distance, 0)]
    }


class ch34tsRus:

    def __init__(self):
        self._last = [Move.UP, Move.RIGHT, Move.DOWN, Move.LEFT]
        self._search_vectors = {
            d: _create_search_vector(d)
            for d in range(1, 32)
        }

    def get_name(self):
        return "Hein Won't Let Me Cheat"

    def get_contributor(self):
        return "Lewie"

    def _pre_process(self, enemies):
        self._position = _Position.fromNumpy(self.position)

        return [
            _Enemy(e['id'], _Position.fromNumpy(e['position']))
            for e in enemies if e['id'] != self.id
        ]

    def _will_win(self, id):
        return (id == 0) or ((self.id - id) % 3 == 2)

    def _should_stay(self, grid, enemies):
        for e in enemies:
            if self._position.distance(e.position) < 3:
                return False

        return self._will_win(grid[self._position.y][self._position.x])

    def _set_last(self, move):
        self._last.remove(move)
        self._last.insert(0, move)
        return move

    def _find_target(self, grid, enemies, game_info):
        winnable = numpy.select([grid != 0], [(self.id - grid) % 3], 2)
        for e in enemies:
            p = e.position
            for y in range(max(0, p.y - 1), min(game_info.grid_size, p.y + 2)):
                for x in range(max(0, p.x - 1),
                               min(game_info.grid_size, p.x + 2)):
                    winnable[y][x] = 0

        for r in range(1, game_info.grid_size):
            vectors = self._search_vectors[r]
            for d in self._last:
                for v in vectors[d]:
                    pos = self._position.add(v)
                    if pos.is_valid(
                            game_info.grid_size) and (winnable[pos.y][pos.x]
                                                      == 2):
                        return pos

        return _Position(x=0, y=0)

    def _get_direction(self, target, grid):
        vector = self._position.vector(target)

        if abs(vector[0]) > abs(vector[1]):
            if vector[0] < 0: return Move.LEFT
            return Move.RIGHT

        if vector[1] < 0: return Move.DOWN
        return Move.UP

    def determine_next_move(self, grid, enemies, game_info):
        enemies = self._pre_process(enemies)

        if self._should_stay(grid, enemies):
            return Move.STAY

        target = self._find_target(grid, enemies, game_info)

        return self._set_last(self._get_direction(target, grid))
