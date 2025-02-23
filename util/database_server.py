import sqlite3
import pandas as pd

class DatabaseSaver:
    def __init__(self, db_name):
        """SQLiteデータベースに接続"""
        self.db_name = db_name

    def save_dataframes(self, dataframes):
        """複数のデータフレームをSQLiteに保存"""
        conn = sqlite3.connect(self.db_name)
        for table_name, df in dataframes.items():
            if not isinstance(df, pd.DataFrame):
                print(f" {table_name} はデータフレームではありません: {type(df)}")
                continue  # データフレームでない場合はスキップ
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        print("保存完了")