# level_utils.py
from bot.db import add_xp, get_level_and_xp, update_level

class LevelUtils:
    @staticmethod
    def add_xp(user_id: int, xp_to_add: int) -> int:
        add_xp(user_id, xp_to_add)
        level, xp = get_level_and_xp(user_id)
        next_level_xp = 100 * (1.1 ** (level - 1))

        if xp >= next_level_xp:
            new_level = level + 1
            new_xp = xp - next_level_xp
            update_level(user_id, new_level, new_xp)
            return new_level
        else:
            return level
