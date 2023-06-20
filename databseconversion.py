import sqlite3
import pandas as pd
df = pd.read_csv('torrents.csv')
df.columns = df.columns.str.strip()
connection = sqlite3.connect("demo.db")
df.to_sql('titles',connection, if_exists='replace',)
exit()
