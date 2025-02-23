import requests
import time
import pandas as pd
from tqdm import tqdm

class FetchPokemonbase:
    def __init__(self, output_file="pokemon_infos.csv"):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"
        self.species_url = "https://pokeapi.co/api/v2/pokemon-species"

        self.output_file = output_file

        self.limit = 1025

    def get_all_pokemon(self):
        """全ポケモンのリストを取得"""
        url = f"{self.base_url}?limit={self.limit}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [pokemon["name"] for pokemon in data["results"]]
        return []

    def get_japanese_name(self, name):
        """ポケモンの日本語名を取得"""
        url = f"{self.species_url}/{name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for name_entry in data["names"]:
                if name_entry["language"]["name"] == "ja":
                    return name_entry["name"]
        return name  # 日本語名が取得できなかった場合は英語名をそのまま使う

    def get_pokemon_data(self, name):
        """ポケモンの基本データを取得"""
        url = f"{self.base_url}/{name}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            japanese_name = self.get_japanese_name(name)

            return {
                "english_name": data["name"],
                "japanese_name": japanese_name,
                "height": data["height"],
                "weight": data["weight"]
            }
        return None

    def save_pokemon_data(self):
        """全ポケモンのデータを取得し、DataFrameとして保存"""
        pokemon_list = self.get_all_pokemon()
        pokemon_data_list = []
        
        for pokemon in tqdm(pokemon_list, desc="Pokémon List Progress"):
            data = self.get_pokemon_data(pokemon)
            if data:
                pokemon_data_list.append(data)
            time.sleep(0.5)
        
        df = pd.DataFrame(pokemon_data_list)
         # CSV に保存
        output_path = f"./data/{self.output_file}"  
        df.to_csv(output_path, index=False, encoding="utf-8")
        
        return output_path
