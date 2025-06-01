from pymongo import MongoClient
from pymongo.database import Database, Collection
import os
from .data import Data, Tournament
from dataclasses import asdict
from dacite import from_dict

# database connection should be instantiated only once
password = os.environ['MONGODB_PASSWORD']
client = MongoClient(f"mongodb+srv://matlewan:{password}@cluster0.vybee.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongodb_pomyslgrandprix = client['pomysl-grandprix']

class Repository:

    def __init__(self):
        self.db: Database = mongodb_pomyslgrandprix
        self.data = self.db['data']
        self.tournaments = self.db['tournaments']
    
    def exist_tournament(self, id) -> bool:
        return self.tournaments.count_documents({"_id": id}) == 1
    
    def save_tournament(self, id: str, tournament: Tournament):
        t = asdict(tournament)
        t['_id'] = id
        self.tournaments.insert_one(t)
    
    def get_data(self) -> Data:
        data_dict = self.data.find_one({'_id': '1'})
        return from_dict(data_class=Data, data=data_dict)
    
    def get_raw_data(self) -> dict:
        return self.data.find_one({'_id': '1'})

    def save_data(self, data: Data):
        d = asdict(data)
        d['_id'] = '1'
        self.data.replace_one({"_id": '1'}, d, upsert=True)

    def get_tournament_ids(self) -> list[str]:
        return [t['id'] for t in self.tournaments.find({}, {'id': 1})]
    
    def get_tournaments(self) -> list[Tournament]:
        return [from_dict(data_class=Tournament, data=t) for t in self.tournaments.find({})]

if __name__ == '__main__':
    repository = Repository()
    # test something
