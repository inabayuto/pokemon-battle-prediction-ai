import pandas as pd
import os


class DataLoader:
    def __init__(self, data_path: str = "../notebook/data/"):
        self.data_path = data_path

    def load(self, filename: str) -> pd.DataFrame:

        if filename == "pokemon_data":
            return self._load_pokemon_data()
        elif filename == "pokemon_training":
            return self._load_pokemon_training()
        elif filename == "pokemon_moves":
            return self._load_pokemon_moves()
        elif filename == "pokemon_infos":
            return self._load_pokemon_infos()
        else:
            print("ファイルは存在しません")

        # return self._load()

    def _load_pokemon_data(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "pokemon_data.csv")

        df = pd.read_csv(file_path)
        df = df.drop_duplicates(subset="Name", keep="first")
        
        # ポケモン名の正規化
        name_corrections = {
            'Nidoran♀': 'nidoran-f',
            'Nidoran♂': 'nidoran-m',
            "Farfetch'd": 'farfetchd',
            "Sirfetch'd": 'sirfetchd',
            "Mr. Mime": 'mr-mime',
            "Mr. Rime": 'mr-rime',
            "Mime Jr.": 'mime-jr',
            "Flabébé": 'flabebe',
            "Type: Null": 'type-null'
        }
        
        df['Name'] = df['Name'].replace(name_corrections)
        df['Name'] = df['Name'].str.replace(' ', '-').str.replace(':', '-')
        
        return df
    
    def _load_pokemon_training(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "pokemon_training.csv")

        df = pd.read_csv(file_path)

        name_corrections = {
            'Nidoran♀': 'nidoran-f',
            'Nidoran♂': 'nidoran-m',
            "Farfetch'd": 'farfetchd',
            "Sirfetch'd": 'sirfetchd',
            "Mr. Mime": 'mr-mime',
            "Mr. Rime": 'mr-rime',
            "Mime Jr.": 'mime-jr',
            "Flabébé": 'flabebe',
            "Type: Null": 'type-null'
        }
        
        df['pokemon_name'] = df['pokemon_name'].replace(name_corrections)
        df['pokemon_name'] = df['pokemon_name'].str.replace(' ', '-').str.replace(':', '-')

        return df
    
    def _load_pokemon_moves(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "pokemon_moves.csv")

        df = pd.read_csv(file_path)

        name_corrections = {
            'Nidoran♀': 'nidoran-f',
            'Nidoran♂': 'nidoran-m',
            "Farfetch'd": 'farfetchd',
            "Sirfetch'd": 'sirfetchd',
            "Mr. Mime": 'mr-mime',
            "Mr. Rime": 'mr-rime',
            "Mime Jr.": 'mime-jr',
            "Flabébé": 'flabebe',
            "Type: Null": 'type-null'
        }
        
        df['Pokemon Name'] = df['Pokemon Name'].replace(name_corrections)
        df['Pokemon Name'] = df['Pokemon Name'].str.replace(' ', '-').str.replace(':', '-')

        return df
    
    def _load_pokemon_infos(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "pokemon_infos.csv")

        df = pd.read_csv(file_path)
        
        return df


    def _load_battles_info(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "battles_info.csv")

        df = pd.read_csv(file_path)

        return df
    
    def _load_players_info(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "players_info.csv")

        df = pd.read_csv(file_path)
        
        return df