from .data import *

def expected_score(opponent_ratings: list[float], own_rating: float) -> float:
    """How many points we expect to score in a tourney with these opponents"""
    return sum(
        1 / (1 + 10**((opponent_rating - own_rating) / 400))
        for opponent_rating in opponent_ratings
    )

def performance_rating(opponent_ratings: list[float], score: float) -> int:
    """Calculate mathematically perfect performance rating with binary search"""
    lo, hi = 0, 4000
    while hi - lo > 1:
        mid = (lo + hi) / 2
        if expected_score(opponent_ratings, mid) < score:
            lo = mid
        else:
            hi = mid
    return round(mid)

def performance_ratings(matches: list[Match], players: dict[str,Player]):
    NO_OPPONENT = "No Opponent"
    score_by_player: dict[str,tuple[int,list]] = {}
    perf_by_player = {}
    for m in matches:
        if m.white == NO_OPPONENT or m.black == NO_OPPONENT:
            continue
        score : tuple[int, list] = score_by_player.get(m.white, (0, []))
        score[1].append(players[m.black].rating)
        score_by_player[m.white] = (score[0] + m.result, score[1])
        score : tuple[int, list] = score_by_player.get(m.black, (0, []))
        score[1].append(players[m.white].rating)
        score_by_player[m.black] = (score[0] + 1.0-m.result, score[1])

    for name, score in score_by_player.items():
        perf_by_player[name] = performance_rating(score[1], score[0])

    s = score_by_player['Lewandowski Mateusz']
    score_by_player = {}
    for m in matches:
        if m.white == NO_OPPONENT or m.black == NO_OPPONENT:
            continue
        score : tuple[int, list] = score_by_player.get(m.white, (0, []))
        score[1].append(perf_by_player.get(m.black, 1000))
        score_by_player[m.white] = (score[0] + m.result, score[1])
        score : tuple[int, list] = score_by_player.get(m.black, (0, []))
        score[1].append(perf_by_player.get(m.white, 1000))
        score_by_player[m.black] = (score[0] + 1-m.result, score[1])

    for name, score in score_by_player.items():
        perf_by_player[name] = performance_rating(score[1], score[0])

    return perf_by_player

if __name__ == "__main__":
    print(performance_rating([1851, 2457, 1989, 2379, 2407, 4000], 5))  # should be 2551