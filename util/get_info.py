import requests
import time
from tqdm import tqdm


class FetchPokemonInfo:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"
    
    def get_all_pokemon(self):
        # 全ポケモンのリストを取得
        url = f"{self.base_url}?limit=1000"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [pokemon["name"] for pokemon in data["results"]]
        return []
    

    def get_pokemon_data(self, name):
        url = f"{self.base_url}/{name}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
        
        # ステータスが6つ未満の場合はデフォルト値を設定
        base_stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        all_stats = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]

        # 欠けているステータスがあれば0を代入
        for stat in all_stats:
            if stat not in base_stats:
                base_stats[stat] = 0  # デフォルト値（0）をセット

            return {
                "name": data["name"],
                "height": data["height"],
                "weight": data["weight"],
                "types": ", ".join(t["type"]["name"] for t in data["types"]),
                "hp": base_stats["hp"],
                "attack": base_stats["attack"],
                "defense": base_stats["defense"],
                "special-attack": base_stats["special-attack"],
                "special-defense": base_stats["special-defense"],
                "speed": base_stats["speed"]
            }
        
    def save_pokemon_data(self):
        pokemon_list = self.get_all_pokemon()
        pokemon_data_list = []
        for i, pokemon in enumerate(tqdm(pokemon_list)):
            data = self.get_pokemon_data(pokemon)
            if data:
                pokemon_data_list.append(data)
            # print(f"[{i+1}/{len(pokemon_list)}] {pokemon} 取得完了")
                
            time.sleep(0.5)
        return pokemon_data_list