"""
Type effectiveness chart for Pokemon battles.
Based on Generation 8+ type chart.
"""

TYPE_CHART = {
    "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
    "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
    "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
    "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5},
    "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5},
    "poison": {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2},
    "ground": {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
    "flying": {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
    "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
    "ghost": {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5},
    "dragon": {"dragon": 2, "steel": 0.5, "fairy": 0},
    "dark": {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5},
    "steel": {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2},
    "fairy": {"fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5}
}


def get_type_effectiveness(attacking_type: str, defending_types: list[str]) -> float:
    """
    Calculate type effectiveness multiplier.
    
    Args:
        attacking_type: The type of the attacking move
        defending_types: List of defending Pokemon's types (1 or 2 types)
    
    Returns:
        Multiplier (0, 0.25, 0.5, 1, 2, or 4)
    """
    if not attacking_type or not defending_types:
        return 1.0
    
    multiplier = 1.0
    attacking_type = attacking_type.lower()
    
    for def_type in defending_types:
        if not def_type:
            continue
        def_type = def_type.lower()
        
        if attacking_type in TYPE_CHART:
            effectiveness = TYPE_CHART[attacking_type].get(def_type, 1.0)
            multiplier *= effectiveness
    
    return multiplier


def get_effectiveness_text(multiplier: float) -> str:
    """Convert multiplier to readable text."""
    if multiplier == 0:
        return "No effect"
    elif multiplier < 0.5:
        return "Not very effective... (0.25x)"
    elif multiplier < 1:
        return "Not very effective (0.5x)"
    elif multiplier == 1:
        return "Normal effectiveness"
    elif multiplier == 2:
        return "Super effective! (2x)"
    else:
        return "Super effective!! (4x)"
