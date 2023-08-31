import stampa
import pandas_ta as ta
import pandas as pd
from secret.secret_man.secret_man import SecretManager as sm
import mysql.connector as my_con
from scriba.scriba.scriba import DbManager as db

plot = stampa.Plot()
table = 'spy'

with my_con.connect(**sm.config(db='finance')) as cnx:
    header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    query = f"""SELECT {", ".join(header)} FROM finance.{table}"""
    print(query)
    crs = cnx.cursor()
    crs.execute(query)
    data = crs.fetchall()
    
    print(f'header:\n\n{header}')
    for _ in data[:20]: print(_)
    df = pd.DataFrame({key : [val[indx] for val in data] for indx, key in enumerate(header)})

    print(df.loc[:20])
    df.index = pd.DatetimeIndex(df['Date'], yearfirst= True)
    print(df.index)


    plot(indicator_ohlc= {ta.sma : df['Close']}, df_ohlc= df)