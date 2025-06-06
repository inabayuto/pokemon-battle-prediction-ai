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
import os

# 現在のディレクトリをsys.pathに追加
sys.path.insert(0, '.')  

from util.data_loader import DataLoader

class FetchPokemonMoves:

    def __init__(self, output_file="pokemon_moves.csv"):
        # 解析するポケモンのリスト
        self.generations = range(1, 10)
        
        # 全てのデータを保存するリスト
        self.all_moves_data = []
        
        # ポケモンリスト
        self.pokemon_list = []
        
        # 出力ファイル名
        self.output_file = output_file

    def fetch_pokemon_moves(self, pokemon, generation):
        """指定したポケモンと世代の技リストを取得"""

        # SSL証明書発行
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # # URLの指定
        url = f"https://pokemondb.net/pokedex/{pokemon.lower()}/moves/{generation}"

        # user-Agentを指定
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

            # ポケモンの名前を取得
            pokemon_name_full = soup.find('h1').text.strip()
            pokemon_name = pokemon_name_full.split(' -')[0]  # "Bulbasaur - Generation 1 learnset" → "Bulbasaur"

            # 結果データを格納する辞書
            moves_data = {
                "pokemon_name": pokemon_name,
                "generation": generation,
                "level_up_moves": [],
                "hm_moves": [],
                "tm_moves": [],
            }

            # `tab-moves-{generation}` の div を動的に取得（最も若い番号の div を取得）
            moves_div = None
            for i in range(1, 22):
                moves_div = soup.find('div', {'id': f'tab-moves-{i}'})
                if moves_div:
                    break  # 見つかればループを終了

            if not moves_div:
                print(f"{pokemon_name} (Gen {generation}) の技情報が見つかりませんでした")
                return None

            # レベルアップ技の取得
            level_up_section = moves_div.find('h3', string='Moves learnt by level up')
            if level_up_section:
                level_up_table = level_up_section.find_next('div', class_='resp-scroll')
                if level_up_table:
                    for row in level_up_table.find_all('tr')[1:]:  # ヘッダーをスキップ
                        cols = row.find_all('td')
                        if len(cols) == 6:
                            moves_data['level_up_moves'].append({
                                "Lv.": cols[0].text.strip(),
                                "Move": cols[1].text.strip(),
                                "Type": cols[2].text.strip(),
                                "Category": cols[3].img['alt'] if cols[3].img else 'N/A',
                                "Power": cols[4].text.strip(),
                                "Accuracy": cols[5].text.strip()
                            })

            # HM技の取得
            hm_section = moves_div.find('h3', string='Moves learnt by HM')
            if hm_section:
                hm_table = hm_section.find_next('div', class_='resp-scroll')
                if hm_table:
                    for row in hm_table.find_all('tr')[1:]:
                        cols = row.find_all('td')
                        if len(cols) == 6:
                            moves_data['hm_moves'].append({
                                "Lv.": cols[0].text.strip(),
                                "Move": cols[1].text.strip(),
                                "Type": cols[2].text.strip(),
                                "Category": cols[3].img['alt'] if cols[3].img else 'N/A',
                                "Power": cols[4].text.strip(),
                                "Accuracy": cols[5].text.strip()
                            })

            # TM技の取得
            tm_section = moves_div.find('h3', string='Moves learnt by TM')
            if tm_section:
                tm_table = tm_section.find_next('div', class_='resp-scroll')
                if tm_table:
                    for row in tm_table.find_all('tr')[1:]:
                        cols = row.find_all('td')
                        if len(cols) == 6:
                            moves_data['tm_moves'].append({
                                "Lv.": cols[0].text.strip(),
                                "Move": cols[1].text.strip(),
                                "Type": cols[2].text.strip(),
                                "Category": cols[3].img['alt'] if cols[3].img else 'N/A',
                                "Power": cols[4].text.strip(),
                                "Accuracy": cols[5].text.strip()
                            })

            # print(f"{pokemon_name} (Gen {generation}) のデータ取得完了")
            return moves_data

        except Exception as e:
            # print(f"{pokemon} (Gen {generation}) のデータ取得に失敗しました: {e}")
            return None
    
    def load_pokemon_data(self):
        """DataLoaderをインスタンス化してデータを読み込む"""
        loader = DataLoader() # インスタンス化
        pokemon_infos = loader.load("pokemon_data") # ポケモンの基本情報データを読み込む
        pokemon_list = pokemon_infos['Name'].tolist() # ポケモン名をリスト化
        self.pokemon_list = pokemon_list # 必要なポケモンリストを設定
        return self.pokemon_list

    def save_pokemon_moves(self):
        """ポケモンごとに世代データを取得"""   
        self.load_pokemon_data() # ポケモンリストをロード
        self.all_moves_data = [] # 空のリストを作成

        # 各ポケモン毎に技を取得
        for pokemon in tqdm(self.pokemon_list, desc="Pokémon List Progress"):
            for gen in self.generations:
                moves = self.fetch_pokemon_moves(pokemon, gen)  # fetch_pokemon_movesをselfで呼び出す
                if moves:
                    self.all_moves_data.append(moves)
        
        return self.all_moves_data

    
    def prepare_moves_data(self):
        """全ポケモンの技データを取得し、DataFrameとして保存"""
        rows = [] # 空のリストを作成
        move_types = ["level_up_moves", "tm_moves", "hm_moves"]  # 識別用のカラムを追加

        for pokemon in self.all_moves_data:
            for move_type in move_types:
                if move_type in pokemon: 
                    for move in pokemon[move_type]:
                        rows.append({
                            "Pokemon Name": pokemon["pokemon_name"],
                            "Generation": pokemon["generation"],
                            "Move Type": move_type,
                            "Lv.": move.get("Lv.", "—"), 
                            "Move": move["Move"],
                            "Type": move["Type"],
                            "Category": move["Category"],
                            "Power": move["Power"],
                            "Accuracy": move["Accuracy"]
                        })

        # DataFrameの作成
        df = pd.DataFrame(rows)

        # フォルダの作成（存在しない場合）
        folder = "data"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filepath = os.path.join(folder, self.output_file)
        
        df.to_csv(filepath, index=False, encoding="utf-8")

        return filepath
        

 
