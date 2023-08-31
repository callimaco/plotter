import stampa
import pandas_ta as ta
import pandas as pd
from secret.secret_man.secret_man import SecretManager as sm
import mysql.connector as my_con
from scriba.scriba.scriba import DbManager as db

plot = stampa.Plot()
table = 'spy'

with my_con.connect(**sm.config(db='finance')) as cnx:

    query = f"""SELECT * FROM finance.{table}"""

    crs = cnx.cursor()
    crs.execute(query)
    data = crs.fetchall()

    query = f"""DESCRIBE finance.{table}"""

    crs = cnx.cursor()
    crs.execute(query)
    header = crs.fetchall()

    header = [name[0] for name in header[1:]]

    df = pd.DataFrame({key : [val[indx] for val in data] for indx, key in enumerate(header)})

    plot(indicator_ohlc= [ta.sma], df_ohlc= df)