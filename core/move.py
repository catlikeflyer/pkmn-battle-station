"""
Move class for Pokemon battles.
"""

import sqlite3
from typing import Optional


class Move:
    """Represents a Pokemon move with its properties."""

    def __init__(self, name: str, db_path: str = "pkmn_battle_station.db"):
        """
        Initialize a Move from the database.

        Args:
            name: Move name (e.g., "thunderbolt")
            db_path: Path to SQLite database
        """
        self.name = name
        self.power: Optional[int] = None
        self.accuracy: Optional[int] = None
        self.pp: int = 0
        self.type: str = "normal"
        self.damage_class: str = "status"
        self.priority: int = 0

        self._load_from_db(db_path)

    def _load_from_db(self, db_path: str):
        """Load move data from database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT power, accuracy, pp, type, damage_class, priority FROM moves_dim WHERE name = ?",
            (self.name,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            (
                self.power,
                self.accuracy,
                self.pp,
                self.type,
                self.damage_class,
                self.priority,
            ) = result

    def is_damaging(self) -> bool:
        """Check if move deals damage."""
        return self.damage_class in ["physical", "special"] and self.power is not None

    def __repr__(self):
        if self.is_damaging():
            return f"Move({self.name}, {self.type}, {self.power} power, {self.accuracy}% acc)"
        return f"Move({self.name}, {self.type}, status)"
