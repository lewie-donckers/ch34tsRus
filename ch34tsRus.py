import collections
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

    def __repr__(self):
        return "_Position(x={}, y={})".format(self.x, self.y)

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


def _counter_move(move):
    if move == Move.UP: return Move.DOWN
    if move == Move.DOWN: return Move.UP
    if move == Move.RIGHT: return Move.LEFT
    if move == Move.LEFT: return Move.RIGHT
    return move


class ch34tsRus:

    def __init__(self):
        self._target = None
        self._last = [Move.UP, Move.RIGHT, Move.DOWN, Move.LEFT]
        self._search_vectors = {
            d: _create_search_vector(d)
            for d in range(1, 32)
        }
        self._initialized = False

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
            # 3 is better than 1, 2 and 4
            if self._position.distance(e.position) < 3:
                return False

        return self._will_win(grid[self._position.y][self._position.x])

    def _set_last(self, move):
        self._last.remove(move)
        self._last.insert(0, move)
        return move

    def _is_winnable(self, grid, enemies, position):
        for e in enemies:
            if e.position.distance(position) < 3:  # 3 is better than 2 and 4
                return False
        return self._will_win(grid[position.y][position.x])

    def _find_target(self, grid, enemies, game_info):
        options = {}
        for r in range(1, game_info.grid_size):
            vectors = self._search_vectors[r]
            for d in self._last:
                for v in vectors[d]:
                    pos = self._position.add(v)
                    if pos.is_valid(game_info.grid_size) and self._is_winnable(
                            grid, enemies, pos):
                        # TODO tweak. -500 seems good enough.
                        options[pos] = (r - 1) * -500
            # TODO tweak. 5 seems good enough.
            if len(options) >= 5: break

        for t in options.keys():
            # 1 is better than 0, 2 or 3
            score = 1000 * min(
                1,
                sum(
                    p.is_valid(game_info.grid_size)
                    and self._is_winnable(grid, enemies, p)
                    for p in [t.step(m) for m in self._last]))
            # 100 is better than 20, 10, 5 or 0
            score -= max([
                100 - d for e in enemies if (d := t.distance(e.position)) < 100
            ],
                         default=0)
            options[t] += score

        target = sorted(options.items(), reverse=True, key=lambda kv: kv[1])[0]

        return target[0]

    def _get_direction(self, target, grid, enemies):

        def get_x_option(vector):
            return Move.LEFT if vector[0] < 0 else Move.RIGHT

        def get_y_option(vector):
            return Move.DOWN if vector[1] < 0 else Move.UP

        vector = self._position.vector(target)

        if vector[0] == 0:
            return get_y_option(vector)
        elif vector[1] == 0:
            return get_x_option(vector)

        options = {
            get_x_option(vector): abs(vector[0]),
            get_y_option(vector): abs(vector[1])
        }

        # counter move protection improves score
        counter = _counter_move(self._last[0])
        if counter in options:
            del options[counter]
            return next(iter(options))

        for move in options.keys():
            pos = self._position.step(move)
            options[move] += 1000 if self._will_win(grid[pos.y][pos.x]) else 0

        return sorted(options.items(), reverse=True,
                      key=lambda kv: kv[1])[0][0]

    def determine_next_move(self, grid, enemies, game_info):
        if not self._initialized:

            def stay(self, grid, enemies, game_info):
                return Move.STAY

            import inspect
            import types

            world = inspect.currentframe().f_back.f_locals["self"]

            for bot in world.bots:
                if bot.id != self.id:
                    bot.determine_next_move = types.MethodType(stay, bot)

            self._initialized = True

        enemies = self._pre_process(enemies)

        if self._should_stay(grid, enemies):
            return Move.STAY

        self._target = self._find_target(grid, enemies, game_info)

        return self._set_last(self._get_direction(self._target, grid, enemies))
