"""
Pokemon class for battle simulation.
"""

import sqlite3
from typing import Optional
from core.move import Move


class Pokemon:
    """Represents a Pokemon with stats, moves, and battle state."""

    def __init__(self, name: str, db_path: str = "data_prep/pkmn_battle_station.db"):
        """
        Initialize a Pokemon from the database.

        Args:
            name: Pokemon name (e.g., "pikachu")
            db_path: Path to SQLite database
        """
        self.name = name
        self.db_path = db_path

        # Base stats
        self.id: int = 0
        self.base_hp: int = 0
        self.base_attack: int = 0
        self.base_defense: int = 0
        self.base_special_attack: int = 0
        self.base_special_defense: int = 0
        self.base_speed: int = 0
        self.type1: str = ""
        self.type2: Optional[str] = None

        # Competitive set
        self.ability: str = ""
        self.item: str = ""
        self.nature: str = "hardy"
        self.evs = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "special_attack": 0,
            "special_defense": 0,
            "speed": 0,
        }

        # Moves
        self.moves: list[Move] = []

        # Battle state
        self.current_hp: int = 0
        self.max_hp: int = 0
        self.status: Optional[str] = None  # paralysis, burn, sleep, etc.
        self.stat_stages = {
            "attack": 0,
            "defense": 0,
            "special_attack": 0,
            "special_defense": 0,
            "speed": 0,
            "accuracy": 0,
            "evasion": 0,
        }

        # Load data
        self._load_base_stats()
        self._load_smogon_set()
        self._calculate_stats()
        self.current_hp = self.max_hp

    def _load_base_stats(self):
        """Load base stats from pokemon_fact table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT id, hp, attack, defense, special_attack, special_defense, speed, type1, type2
               FROM pokemon_fact WHERE name = ?""",
            (self.name,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            (
                self.id,
                self.base_hp,
                self.base_attack,
                self.base_defense,
                self.base_special_attack,
                self.base_special_defense,
                self.base_speed,
                self.type1,
                self.type2,
            ) = result
        else:
            raise ValueError(f"Pokemon '{self.name}' not found in database")

    def _load_smogon_set(self):
        """Load competitive moveset from smogon_sets table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT ability, item, nature, move1, move2, move3, move4,
                      ev_hp, ev_attack, ev_defense, ev_special_attack, ev_special_defense, ev_speed
               FROM smogon_sets WHERE pokemon_name = ?""",
            (self.name,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            (
                self.ability,
                self.item,
                self.nature,
                move1,
                move2,
                move3,
                move4,
                ev_hp,
                ev_atk,
                ev_def,
                ev_spatk,
                ev_spdef,
                ev_spd,
            ) = result

            self.evs = {
                "hp": ev_hp or 0,
                "attack": ev_atk or 0,
                "defense": ev_def or 0,
                "special_attack": ev_spatk or 0,
                "special_defense": ev_spdef or 0,
                "speed": ev_spd or 0,
            }

            # Load moves
            for move_name in [move1, move2, move3, move4]:
                if move_name:
                    try:
                        self.moves.append(Move(move_name, self.db_path))
                    except Exception as e:
                        print(f"Warning: Could not load move '{move_name}': {e}")

    def _calculate_stats(self, level: int = 100):
        """
        Calculate actual stats from base stats, EVs, IVs (assumed max), and nature.
        Uses Pokemon stat formula.
        """
        iv = 31  # Assume perfect IVs

        # HP calculation
        if self.base_hp > 0:
            self.max_hp = (
                int(((2 * self.base_hp + iv + self.evs["hp"] // 4) * level) / 100)
                + level
                + 10
            )
        else:
            self.max_hp = 1

        # Other stats (with nature modifiers)
        self.attack = self._calc_stat(
            self.base_attack, self.evs["attack"], iv, level, "attack"
        )
        self.defense = self._calc_stat(
            self.base_defense, self.evs["defense"], iv, level, "defense"
        )
        self.special_attack = self._calc_stat(
            self.base_special_attack,
            self.evs["special_attack"],
            iv,
            level,
            "special_attack",
        )
        self.special_defense = self._calc_stat(
            self.base_special_defense,
            self.evs["special_defense"],
            iv,
            level,
            "special_defense",
        )
        self.speed = self._calc_stat(
            self.base_speed, self.evs["speed"], iv, level, "speed"
        )

    def _calc_stat(
        self, base: int, ev: int, iv: int, level: int, stat_name: str
    ) -> int:
        """Calculate individual stat with nature modifier."""
        stat = int(((2 * base + iv + ev // 4) * level) / 100) + 5

        # Apply nature modifier (simplified - would need full nature chart)
        nature_boosts = {
            "adamant": {"attack": 1.1, "special_attack": 0.9},
            "modest": {"special_attack": 1.1, "attack": 0.9},
            "jolly": {"speed": 1.1, "special_attack": 0.9},
            "timid": {"speed": 1.1, "attack": 0.9},
            # Add more natures as needed
        }

        if self.nature in nature_boosts and stat_name in nature_boosts[self.nature]:
            stat = int(stat * nature_boosts[self.nature][stat_name])

        return stat

    def get_types(self) -> list[str]:
        """Get list of types."""
        return [t for t in [self.type1, self.type2] if t]

    def take_damage(self, damage: int):
        """Reduce current HP by damage amount."""
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self) -> bool:
        """Check if Pokemon has fainted."""
        return self.current_hp <= 0

    def hp_percentage(self) -> float:
        """Get current HP as percentage."""
        return (self.current_hp / self.max_hp) * 100 if self.max_hp > 0 else 0

    def __repr__(self):
        return f"Pokemon({self.name}, {self.type1}/{self.type2 or 'None'}, HP: {self.current_hp}/{self.max_hp})"
