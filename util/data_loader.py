import pandas as pd
import os


class DataLoader:
    def __init__(self, data_path: str = "../notebook/data/"):
        self.data_path = data_path

    def load(self) -> pd.DataFrame:
        return self._load()

    def _load(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_path, "pokemon_info.csv")

        # CSVファイルをDataFrameとして読み込む
        pokemon_infos = pd.read_csv(file_path)

        # 名前が複数あるポケモンの名前を一つに統一
        pokemon_infos["name"] = pokemon_infos.name.apply(lambda x: x.split("-")[0])
        pokemon_infos = pokemon_infos.drop_duplicates(subset="name", keep="first")

        # 複数あるtypeをリストで所持
        pokemon_infos["types"] = pokemon_infos["types"].fillna("")
        pokemon_infos["types"] = pokemon_infos["types"].astype(str)
        pokemon_infos["types"] = pokemon_infos.types.apply(lambda x: x.split(","))
        return pokemon_infos