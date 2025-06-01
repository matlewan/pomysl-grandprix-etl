from dataclasses import dataclass

@dataclass
class Match:
    white : str
    black : str
    result : float

@dataclass
class Result:
    player : str
    place : int
    points : float
    bch1 : float
    bch : float

@dataclass
class Player:
    name : str
    title : str
    club : str
    birthdate : int
    rating : float
    id : int = 0
    pomysl_rating : float = 0.0  # Rating calculated based on result in Pomysł GrandPrix
    performance : float = 0.0
    score : float = 0.0
    M: int = 0
    W: int = 0
    D: int = 0
    L: int = 0

@dataclass
class Round:
    num: int
    matches: list[Match]

@dataclass
class Tournament:
    id : str
    name : str
    date : str
    time_control : str
    n_rounds: int
    players: list[Player]
    rounds: list[Round]
    results: list[Result]

@dataclass
class Duel:
    player : str
    opponent : str
    W : int
    D : int
    L : int

@dataclass
class Data:
    tournaments : dict[str,Tournament]
    players: dict[str,Player]
    duels: list[Duel]
