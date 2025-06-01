import requests
import base64
import os
import json

from .data import Data

class GithubRepository:
    def save_data(self, data: Data) -> bool:
        str_data = json.dumps(data, default=lambda o: o.__dict__)
        return self.__save_file("pomysl-grandprix/out.json", str_data)
    
    def __save_file(self, path: str, content: str) -> bool:
        # Parametry
        token = os.environ['GITHUB_API_TOKEN']
        owner = "matlewan"
        repo = "matlewan.github.io"
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

        # Nowa zawartość pliku (w formacie Base64)
        base64_content = base64.b64encode(content.encode(encoding='utf-8')).decode(encoding='utf-8')

        # Pobierz SHA istniejącego pliku
        headers = {"Authorization": f"token {token}"}
        response = requests.get(api_url, headers=headers)
        file_info = response.json()
        sha = file_info["sha"]

        # Zaktualizuj plik
        data = {
            "message": "Zaktualizowano plik za pomocą API",
            "content": base64_content,
            "sha": sha
        }
        update_response = requests.put(api_url, json=data, headers=headers)
        return update_response.status_code in [200,201]

