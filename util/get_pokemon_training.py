import ssl
import certifi
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
from os import write
import urllib.request
from bs4.dammit import encoding_res 
import pandas as pd
import sys
import json
# 現在のディレクトリをsys.pathに追加
sys.path.insert(0, '..')  

from util.data_loader import DataLoader


class FetchPokemonTraining:

    def __init__(self, output_file="pokemon_training.csv"):
        # 出力ファイル名
        self.output_file = output_file

    def fetch_pokemon_training(self, pokemon):
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        """指定したポケモンのリストのトレーニングデータを取得"""
        all_pokemon_data = []

 
        url = f"https://pokemondb.net/pokedex/{pokemon.lower()}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }

        try:
            # HTMLデータを取得
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, context=ssl_context)
            html = response.read().decode("utf-8")

            # BeautifulSoupで解析
            soup = BeautifulSoup(html, 'html.parser')

            # ポケモン名の取得
            pokemon_name_full = soup.find('h1').text.strip()
            pokemon_name = pokemon_name_full.split(' -')[0]

            # 結果データを格納する辞書
            training_data = {"pokemon_name": pokemon_name}

            # h2タグを検索し、"Training" セクションを探す
            h2_tags = soup.find_all('h2')
            for h2 in h2_tags:
                if 'Training' in h2.text:
                    training_table = h2.find_next("table", class_="vitals-table")

                    if training_table:
                        for row in training_table.find_all("tr"):
                            th = row.find("th")
                            td = row.find("td")

                            if th and td:
                                key = th.text.strip()
                                value = td.text.strip()
                                training_data[key] = value
                    break
            
            # 取得したポケモンデータをリストに追加
            all_pokemon_data.append(training_data)

        except Exception as e:
            print(f"{pokemon} のHTML取得に失敗しました: {e}")

        # JSONリスト形式で返す
        return json.dumps(all_pokemon_data, indent=4, ensure_ascii=False)


    def load_pokemon_data(self):
        # DataLoaderをインスタンス化してデータを読み込む
        loader = DataLoader()
        pokemon_infos = loader.load("pokemon_data")
        pokemon_list = pokemon_infos['Name'].tolist()
        self.pokemon_list = pokemon_list  # 必要なポケモンリストを設定
        return self.pokemon_list
    
    def save_pokemon_training(self):
        # ポケモンリストをロード
        self.load_pokemon_data()

        all_training_data = []  # すべてのポケモンのデータを保存するリスト

        for pokemon in tqdm(self.pokemon_list, desc="Pokémon List Progress"):
            training_json = self.fetch_pokemon_training(pokemon)
            training_list = json.loads(training_json)
            all_training_data.extend(training_list)  # データをリストに追加

        # データフレームに変換
        df = pd.DataFrame(all_training_data)

        # CSV に保存
        output_path = f"./data/{self.output_file}"  
        df.to_csv(output_path, index=False, encoding="utf-8")
        
        return output_path
