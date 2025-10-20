-- Stores base stats, types, and abilities
CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    special_attack INTEGER,
    special_defense INTEGER,
    speed INTEGER,
    type1 TEXT,
    type2 TEXT
);

-- Stores all moves and their properties
CREATE TABLE IF NOT EXISTS moves (
    name TEXT PRIMARY KEY,
    power INTEGER,
    accuracy INTEGER,
    pp INTEGER,
    type TEXT,
    damage_class TEXT,  -- 'physical', 'special', or 'status'
    priority INTEGER
);

-- Stores the type effectiveness matrix
CREATE TABLE IF NOT EXISTS type_effectiveness (
    attacking_type TEXT,
    defending_type TEXT,
    multiplier REAL,
    PRIMARY KEY (attacking_type, defending_type)
);