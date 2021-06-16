import pandas as pd
from pandas import *
import sqlalchemy


db = sqlalchemy.create_engine('sqlite:///mah_db.db')
connection = db.raw_connection()
c = connection.cursor()

c.execute("CREATE TABLE database__model (id INTEGER ,description TEXT NOT NULL,qty_type TEXT,price REAL,PRIMARY KEY(id));")

xlsx_mah = pd.read_excel('Summary.xlsx', engine='openpyxl')
xlsx_mah.to_sql('database__model', db, if_exists='append', index=False)
