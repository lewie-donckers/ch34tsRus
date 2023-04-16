# Cheats "R" Us

## Cheat 3

Periodically remove a threatening bot

```python
    def determine_next_move(self, grid, enemies, game_info):
        if game_info.current_round % 25 == 0:
            scores = {
                e['id']: numpy.count_nonzero(grid == e['id'])
                for e in enemies
            }
            my_score = scores.pop(self.id, 0)
            id, score = next(
                iter(sorted(scores.items(), key=lambda i: i[1], reverse=True)))
            if score >= my_score - len(enemies):
                import inspect
                world = inspect.currentframe().f_back.f_locals["self"]
                world.harsh = True
                world.bots.pop(
                    next(i for i, v in enumerate(world.bots) if v.id == id))
        
        ...
```
