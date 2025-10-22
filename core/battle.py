"""
Battle simulator for Pokemon fights.
"""

import random
from typing import Optional, Tuple
from core.pokemon import Pokemon
from core.move import Move
from core.type_chart import get_type_effectiveness


class Battle:
    """Simulates a 1v1 Pokemon battle."""

    def __init__(self, pokemon1: Pokemon, pokemon2: Pokemon):
        """
        Initialize a battle between two Pokemon.

        Args:
            pokemon1: First Pokemon
            pokemon2: Second Pokemon
        """
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.turn = 0
        self.battle_log: list[str] = []
        self.winner: Optional[Pokemon] = None

    def simulate(self, max_turns: int = 100) -> Tuple[Optional[Pokemon], list[str]]:
        """
        Simulate the entire battle.

        Args:
            max_turns: Maximum number of turns before declaring a draw

        Returns:
            Tuple of (winner, battle_log)
        """
        self.battle_log.append(
            f"Battle Start: {self.pokemon1.name} vs {self.pokemon2.name}!"
        )
        self.battle_log.append("")

        while self.turn < max_turns:
            self.turn += 1

            # Determine turn order (based on speed and move priority)
            first, second = self._determine_turn_order()

            # First Pokemon attacks
            if not self._execute_turn(first, second):
                break

            # Check if second Pokemon fainted
            if second.is_fainted():
                self.winner = first
                break

            # Second Pokemon attacks
            if not self._execute_turn(second, first):
                break

            # Check if first Pokemon fainted
            if first.is_fainted():
                self.winner = second
                break

        # Battle ended
        if self.winner:
            self.battle_log.append("")
            self.battle_log.append(f"🏆 {self.winner.name} wins!")
        else:
            self.battle_log.append("")
            self.battle_log.append("Battle ended in a draw (max turns reached)")

        return self.winner, self.battle_log

    def _determine_turn_order(self) -> Tuple[Pokemon, Pokemon]:
        """
        Determine which Pokemon goes first based on speed.
        In the future, can consider move priority.
        """
        if self.pokemon1.speed >= self.pokemon2.speed:
            return self.pokemon1, self.pokemon2
        else:
            return self.pokemon2, self.pokemon1

    def _execute_turn(self, attacker: Pokemon, defender: Pokemon) -> bool:
        """
        Execute one Pokemon's turn.

        Returns:
            False if battle should end, True otherwise
        """
        if attacker.is_fainted():
            return True

        # Select move (for now, use simple AI)
        move = self._select_move(attacker, defender)

        if not move:
            self.battle_log.append(f"{attacker.name} has no valid moves!")
            return False

        self.battle_log.append(f"Turn {self.turn}: {attacker.name} used {move.name}!")

        # Check if move hits (accuracy check)
        if not self._check_accuracy(move):
            self.battle_log.append(f"  {attacker.name}'s attack missed!")
            return True

        # Calculate and apply damage
        if move.is_damaging():
            damage = self._calculate_damage(attacker, defender, move)
            defender.take_damage(damage)

            effectiveness = get_type_effectiveness(move.type, defender.get_types())
            eff_text = self._get_effectiveness_text(effectiveness)

            self.battle_log.append(
                f"  {defender.name} took {damage} damage! {eff_text}"
            )
            self.battle_log.append(
                f"  {defender.name}: {defender.current_hp}/{defender.max_hp} HP ({defender.hp_percentage():.1f}%)"
            )

            if defender.is_fainted():
                self.battle_log.append(f"  {defender.name} fainted!")
        else:
            # Status move (simplified)
            self.battle_log.append(f"  {move.name} effect applied!")

        return True

    def _select_move(self, attacker: Pokemon, defender: Pokemon) -> Optional[Move]:
        """
        AI to select best move (simplified).
        Later, this can be replaced with NEAT neural network.
        """
        if not attacker.moves:
            return None

        # Simple AI: Choose move with highest expected damage
        best_move = None
        best_score = -1

        for move in attacker.moves:
            if move.is_damaging():
                # Calculate expected damage as score
                damage = self._calculate_damage(attacker, defender, move)
                effectiveness = get_type_effectiveness(move.type, defender.get_types())
                accuracy = move.accuracy / 100 if move.accuracy else 1.0

                score = damage * effectiveness * accuracy

                if score > best_score:
                    best_score = score
                    best_move = move

        # If no damaging move found, pick first move
        return best_move or attacker.moves[0]

    def _check_accuracy(self, move: Move) -> bool:
        """Check if move hits based on accuracy."""
        if move.accuracy is None:
            return True  # Moves like Swift never miss

        return random.randint(1, 100) <= move.accuracy

    def _calculate_damage(
        self, attacker: Pokemon, defender: Pokemon, move: Move
    ) -> int:
        """
        Calculate damage using Pokemon damage formula (simplified).
        Formula: ((2 * Level / 5 + 2) * Power * A/D / 50 + 2) * Modifiers
        """
        if not move.is_damaging() or move.power is None:
            return 0

        level = 100
        power = move.power

        # Determine attack and defense stats to use
        if move.damage_class == "physical":
            attack = attacker.attack
            defense = defender.defense
        else:  # special
            attack = attacker.special_attack
            defense = defender.special_defense

        # Base damage calculation
        damage = ((2 * level / 5 + 2) * power * attack / defense / 50) + 2

        # STAB (Same Type Attack Bonus)
        if move.type in attacker.get_types():
            damage *= 1.5

        # Type effectiveness
        effectiveness = get_type_effectiveness(move.type, defender.get_types())
        damage *= effectiveness

        # Random factor (0.85 to 1.0)
        damage *= random.uniform(0.85, 1.0)

        # Critical hit (6.25% chance for 1.5x damage)
        if random.random() < 0.0625:
            damage *= 1.5
            self.battle_log.append("  A critical hit!")

        return int(damage)

    def _get_effectiveness_text(self, multiplier: float) -> str:
        """Get effectiveness message."""
        if multiplier == 0:
            return "It had no effect..."
        elif multiplier < 0.5:
            return "It's not very effective..."
        elif multiplier < 1:
            return "It's not very effective..."
        elif multiplier == 2:
            return "It's super effective!"
        elif multiplier > 2:
            return "It's super effective!!"
        return ""
