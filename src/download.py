import bs4
import json
import os
from dacite import from_dict
import re
import requests
from .repository import Repository
from src.data import *

def read_table(url: str) -> list[list[str]]:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    return [[td.text.strip() for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]

def is_na(text: str):
    return text == '' or text is None

def download_players(tournament_url : str) -> list[Result]:
    print(' - players')
    rows = read_table(f'{tournament_url}/players')
    players = []
    for row in rows:
        _,_,title,name,club,rating,birthdate,_ = row
        b = 0 if is_na(birthdate) else int(birthdate)
        r = 1000 if is_na(rating) else int(rating)
        t = "" if is_na(title) else title
        c = "" if is_na(club) else club
        r = Player(norm_player(name), t, c, b, r)
        players.append(r)
    return players

def norm_player(player):
    try:
        p = re.sub(r', ?', ' ', player)
        return re.sub(r'\(.*', '', p).strip()
    except:
        return player


def download_rounds(tournament_url : str, n_rounds : int) -> list[Match]:
    rounds = []
    for n_round in range(1,n_rounds+1):
        print(' - round', n_round)
        round = Round(n_round, [])
        rows = read_table(f"{tournament_url}/rounds/{n_round}")
        for row in rows:
            _, _, _, player1, _, _, result, _, _, player2, _, _, _ = row
            if player1 == '' and player2 == '':
                continue # weird case in tournament #34.1, round 7 (empty row)
            white = norm_player(player1)
            black = norm_player(player2)
            result = {'0':0.0, '1':1.0}.get(result.split()[0], 0.5)
            m = Match(white, black, result)
            round.matches.append(m)
        rounds.append(round)
    return rounds

def download_results(tournament_url : str) -> list[Result]:
    print(' - results')
    rows = read_table(f'{tournament_url}/results')
    results = []
    for row in rows:
        try:
            place, _, _, title, player, _, _, _, pts, bch1, bch, _, _, _, _, _ = row
        except:
            place, _, _, title, player, _, _, _, pts, _, _, _, _ = row
            bch1 = bch = 0
        r = Result(norm_player(player), int(float(place)), float(pts), float(bch1), float(bch))
        results.append(r)
    return results

def download_tournaments(filter_url : str) -> list[Tournament]:
    offset = 0
    tournaments = []
    while True:
        print(f"Offset: {offset}")
        t = download_tournaments_page(filter_url, offset)
        if t == []:
            break # no tournaments on page with given offset
        tournaments += t
        offset += 50
    print()
    return tournaments

def download_tournaments_page(url : str, offset: int) -> list[Tournament]:
    tournaments = []
    resp = requests.get(f"{url}&offset={offset}")
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    for a in soup.select('a.red.card'):
        text = a.text
        id = a.attrs['href'].split('/')[-1]
        tname = re.findall(r'Pomysł GrandPrix \S+', text)[0]
        date = re.findall(r'\d?\d/\d?\d/\d\d', text)[0]
        assert re.match(r'\d?\d/\d?\d/\d\d', date)
        month, day, year = map(int, date.split('/'))
        date = f"{day:02d}.{month:02d}.20{year:02d}"
        # players = int(re.findall(r'\d+\s+players', text)[0].split()[0])
        rounds_str = re.findall(r'\d+/\d+\s+rounds', text)[0]
        rounds_total = int(rounds_str.split()[0].split('/')[1])
        time_control = re.findall(r'players\s+\S+', text)[0].split()[1]
        t = Tournament(id, tname, date, time_control, rounds_total, None, None, None)
        tournaments.append(t)
    return tournaments

def load(directory: str) -> list[Tournament]:
    os.makedirs(directory, exist_ok=True)
    tournaments = []
    for filename in os.listdir(directory):
        with open(f"{directory}/{filename}") as f:
            tournament = from_dict(data_class=Tournament, data=json.load(f))
            tournaments.append(tournament)
    return tournaments

def save_in_filesystem(directory: str, tournaments: list[Tournament]):
    os.makedirs(directory, exist_ok=True)
    for tournament in tournaments:
        filename = f"{directory}/{tournament.name}.json"
        with open(filename, 'w') as f:
            f.write(json.dumps(tournament, default=lambda o: o.__dict__))

def download(url: str, tournament_ids: list[str]):
    downloaded_tournaments = download_tournaments(url)
    for t in downloaded_tournaments:
        if t.id in tournament_ids:
            continue
        url = f"https://www.chessmanager.com/en/tournaments/{t.id}"
        print(t.name, url)
        t.results = download_results(url)
        t.rounds = download_rounds(url, t.n_rounds)
        t.players = download_players(url)
        save_in_filesystem(directory, [t])

def download_and_save_tournaments():
    url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix'
    repository = Repository()
    tournament_ids = repository.get_tournament_ids()
    new_tournaments = download(url, tournament_ids)
    for t in new_tournaments:
        repository.save_tournament(t.name.split()[-1], t)
    
if __name__ == "__main__":
    url = 'https://www.chessmanager.com/en/tournaments?name=Pomys%C5%82+GrandPrix'
    directory = 'data/pomysl-grand-prix/tournaments'
    tournament_ids = [t.id for t in load(directory)]
    new_tournaments = download(url, tournament_ids)
