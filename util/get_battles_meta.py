import requests
import pandas as pd
import re
import os

class FetchBattlesMeta:
    def __init__(self, range=10):
        # APIからバトルのリプレイ一覧を取得
        try:
            response = requests.get("https://replay.pokemonshowdown.com/search.json")
            response.raise_for_status()
            self.replays = response.json()
        except requests.RequestException as e:
            print(f"リプレイデータの取得に失敗しました: {e}")
            self.replays = []

        # 出力フォルダを作成
        os.makedirs("./data", exist_ok=True)
        self.range = range

    # バトルの基本情報を取得
    def get_battle_info(self):
        output_file = "./data/battles_info.csv"
        all_match_info = []

        for replay in self.replays[:self.range]:  # 最新10件のみ取得
            replay_id = replay.get("id")
            if not replay_id:
                continue  # IDがない場合はスキップ

            # リプレイ URL
            replay_url = f"https://replay.pokemonshowdown.com/{replay_id}"
            log_url = f"{replay_url}.json"

            # 対戦ログを取得
            try:
                log_response = requests.get(log_url)
                log_response.raise_for_status()
                battle_log = log_response.json()
            except requests.RequestException as e:
                print(f"バトルログ取得失敗 ({replay_id}): {e}")
                continue

            # メタ情報を取得
            replay_id = battle_log.get("id", "Unknown")
            rule = battle_log.get("format", "Unknown")
            players = battle_log.get("players", ["Unknown", "Unknown"])
            upload_time = battle_log.get("uploadtime", "Unknown")
            rating = battle_log.get("rating", "Unknown")
            formatid = battle_log.get("formatid", "Unknown")

            # 勝者を取得
            log_lines = battle_log.get("log", "")
            winner_match = re.search(r"\|win\|([^\n]+)", log_lines)
            winner = winner_match.group(1) if winner_match else "Unknown"

            # データ保存用リストに追加
            all_match_info.append({
                "Battleid": replay_id,
                "Format": rule,
                "Player1": players[0],
                "Player2": players[1],
                "Winner": winner,
                "Upload Time": upload_time,
                "Rating": rating,
                "Format ID": formatid,
                "Replay URL": replay_url
            })

        # CSVに保存
        if all_match_info:
            match_info_df = pd.DataFrame(all_match_info)
            match_info_df.to_csv(output_file, index=False, encoding="utf-8")
            # print(f"バトル情報を {output_file} に保存しました")
            return output_file
        else:
            print("バトル情報が取得できませんでした")
            return None

    # 各バトルIDごとのプレイヤー情報を取得
    def get_players_info(self):
        output_file = "./data/players_info.csv"
        all_players_info = []

        for replay in self.replays[:self.range]:  # 最新10件のみ取得
            replay_id = replay.get("id")
            if not replay_id:
                continue  # IDがない場合はスキップ

            # リプレイ URL
            replay_url = f"https://replay.pokemonshowdown.com/{replay_id}"
            log_url = f"{replay_url}.json"

            # 対戦ログを取得
            try:
                log_response = requests.get(log_url)
                log_response.raise_for_status()
                battle_log = log_response.json()
            except requests.RequestException as e:
                print(f"バトルログ取得失敗 ({replay_id}): {e}")
                continue

            # メタ情報を取得
            replay_id = battle_log.get("id", "Unknown")
            players = battle_log.get("players", ["Unknown", "Unknown"])
            log_lines = battle_log.get("log", "")

            # 各プレイヤーの使用ポケモンを取得
            player_1_pokemon = re.findall(r"\|poke\|p1\|([^|]+)", log_lines)
            player_2_pokemon = re.findall(r"\|poke\|p2\|([^|]+)", log_lines)

            # CSV出力時のリスト形式調整
            player_1_pokemon_str = ", ".join(player_1_pokemon)
            player_2_pokemon_str = ", ".join(player_2_pokemon)

            # データ保存用リストに追加
            all_players_info.append({
                "Battleid": replay_id,
                "Player1": players[0],
                "Player2": players[1],
                "Player1_Pokemon": player_1_pokemon_str,
                "Player2_Pokemon": player_2_pokemon_str
            })

        # CSVに保存
        if all_players_info:
            players_info_df = pd.DataFrame(all_players_info)
            players_info_df.to_csv(output_file, index=False, encoding="utf-8")
            # print(f"プレイヤー情報を {output_file} に保存しました")
            return output_file
        else:
            print("プレイヤー情報が取得できませんでした")
            return None