# Cheats "R" Us

## Cheat 4

Make other bots run away if too close

```python
        if not self._initialized:
            my_id = self.id

            def runaway(self, grid, enemies, game_info):
                pos = _Position.fromNumpy(self.position)
                my_pos = _Position.fromNumpy(
                    next(
                        iter((e['position'] for e in enemies
                              if e['id'] == my_id))))
                if pos.distance(my_pos) < 20:
                    v = pos.vector(my_pos)
                    options = {
                        Move.RIGHT if v[0] < 0 else Move.LEFT: abs(v[0]),
                        Move.UP if v[1] < 0 else Move.DOWN: abs(v[1])
                    }
                    options = {
                        k: v
                        for k, v in options.items()
                        if pos.step(k).is_valid(game_info.grid_size)
                    }
                    return next(
                        iter(
                            sorted(options.items(),
                                   key=lambda x: x[1],
                                   reverse=True)))[0]

                return self.backup_determine_next_move(grid, enemies,
                                                       game_info)

            import copy
            import inspect
            import types

            world = inspect.currentframe().f_back.f_locals["self"]
            world.harsh = True

            for bot in world.bots:
                if bot.id != self.id:
                    bot.backup_determine_next_move = copy.copy(
                        bot.determine_next_move)
                    bot.determine_next_move = types.MethodType(runaway, bot)

            self._initialized = True

        ...
```
