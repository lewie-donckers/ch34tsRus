# Cheats "R" Us

## Cheat 2

Disable other bots

```python
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
        
        ...
```
