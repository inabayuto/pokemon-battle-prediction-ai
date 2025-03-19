import ssl
import certifi
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
from os import write
import urllib.request
from bs4.dammit import encoding_res 
import pandas as pd
import os
import time
from tqdm import tqdm

class FetchPokemonInfo:
    def __init__(self, output_file="pokemon_data.csv"):

        # 出力ファイル名を初期化
        self.output_file = output_file
        
        # URLの指定
        self.base_url = "https://pokemondb.net/pokedex/all"

    def get_pokemon_data(self):
        """ポケモンの基本情報データを取得"""
        # SSL証明書発行
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # user-Agentを指定
        url = self.base_url
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }

        try:
            # URLリクエストとレスポンスを取得
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, context=ssl_context)

            # HTMLデータを取得
            html = response.read().decode("utf-8")

            # BeautifulSoupで解析
            soup = BeautifulSoup(html, 'html.parser')

            pokemon_data = []
            table = soup.find("table", class_="data-table")
            for row in tqdm(table.find("tbody").find_all("tr"), desc="Pokémon List Progress"):
                columns = row.find_all("td")
                dex_number = columns[0].find("span").text
                name = columns[1].find("a").text
                types = [t.text for t in columns[2].find_all("a")]
                base_stats = [int(columns[i].text) for i in range(3, 9)]

                pokemon_data.append([
                    dex_number, name, types[0], types[1] if len(types) > 1 else None,
                    *base_stats
                ])

                # サーバーへの負荷を避ける為に短い遅延を挿入
                time.sleep(0.5)

                # カラム名の指定
                columns = ["Dex Number", "Name", "Type 1", "Type 2", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

                # DataFrameに変換
                df = pd.DataFrame(pokemon_data, columns=columns)

                return df
        except Exception as e:
            return None

    def save_pokemon_data(self):
        """全ポケモンのデータを取得し、DataFrameとして保存"""
        # フォルダの作成（存在しない場合）
        folder = "data"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filepath = os.path.join(folder, self.output_file)

        df = self.get_pokemon_data()
        
        df.to_csv(filepath, index=False, encoding="utf-8")

        return filepath