import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Any, Union, List, Dict, Optional

import json
import datetime

import pandas as pd
import pandas_ta


# Brain storm 
#   This version of the code takes data from json file, I need to take data from database.
#   In database data still have to be casted to datetime
#   Also there's to find a way to organize the db such that I pass to this code only time series tables
#   A method to handle milliseconds data should be implemented
#######################################################################################################################################################################

IndicatorList : Union[List[str], str]

from typing import Any, List, Optional, Callable

class Plot:
    def __init__(self):
        self.fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.06, subplot_titles=('OHLC', 'Volume'), 
                    row_width=[0.3, 1.2])

    def __call__(self,
                 indicator_ohlc: List[Callable[[pd.DataFrame], Any]],
                 indicator_vol: Optional[List[Callable[[pd.DataFrame], Any]]],
                 df_ohlc: pd.DataFrame, volume: Optional[pd.DataFrame]) -> Any:

        self.fig.add_trace(go.Candlestick(x=df_ohlc.index, open=df_ohlc['Open'], high=df_ohlc['High'],
                low=df_ohlc['Low'], close=df_ohlc['Close'], name="ETHBTC", showlegend=False), 
                row=1, col=1)

        for indicator in indicator_ohlc:
            self.fig.add_trace(
                              go.Scatter(
                                        x=df_ohlc.index,
                                        y=indicator(df_ohlc),
                                        mode='lines',
                                        line=dict(width=1),
                                        name=indicator.__name__),
                              row=1,
                              col=1
                              )
            
        if volume is not None:
            for indicator in indicator_vol:
                self.fig.add_trace(
                                go.Scatter(
                                            x=volume.index,
                                            y=indicator(volume),
                                            mode='lines',
                                            line=dict(width=1),
                                            name=indicator.__name__),
                                row=2,
                                col=1
                                )
        
        self.fig.update(layout_xaxis_rangeslider_visible=False)
        self.fig.show(config=config)

# Rest of your code to call and render the Plot class


    def ohlc(self, df : pd.DataFrame, indicator: IndicatorList) -> None:
        
        if not isinstance(indicator, IndicatorList): 
            raise TypeError('Use Union[List[str], str]')
        



                

        lambda indctr : next(indctr) if isinstance(indicator, List[str]) else indicator


        # Assuming df is your DataFrame

        self.fig.add_trace(go.Scatter(x=df['date'],
                                y= getattr(pandas_ta, next(indicator) if True else False),
                                mode='lines',
                                line=dict(width=1),
                                name='MA7'), row=1, col=1)

        self.fig.add_trace(go.Scatter(x=df['date'],
                                y= ((df['open'] + df['close'] + df['high'] + df['low'])/4).rolling(window=15).mean(),
                                mode='lines',
                                line=dict(width=1),
                                name='MA15'), row=1, col=1)

        self.fig.add_trace(go.Scatter(x=df['date'],
                                y= ((df['open'] + df['close'] + df['high'] + df['low'])/4).rolling(window=33).mean(),
                                mode='lines',
                                line=dict(width=1),
                                name='MA33'), row=1, col=1)


        # Bar trace for volumes on 2nd row without legend
        self.fig.add_trace(go.Bar(x=df['date'], y=df['volume'], showlegend=False), row=2, col=1)

        self.fig.add_trace(go.Scatter(x=df['date'],
                                y= (df['volume']).rolling(window=7).mean(),
                                mode='lines',
                                line=dict(width=1),
                                name='MA7'), row=2, col=1)

        self.fig.add_trace(go.Scatter(x=df['date'],
                                y= (df['volume']).rolling(window=15).mean(),
                                mode='lines',
                                line=dict(width=1),
                                
                                name='MA15'), row=2, col=1)

        self.fig.add_trace(go.Scatter(x=df['date'],
                                y= (df['volume']).rolling(window=33).mean(),
                                mode='lines',
                                line=dict(width=1),
                                name='MA33'), row=2, col=1)
        self.fig.update(layout_xaxis_rangeslider_visible=False)
        self.fig.show(config=config)
        

        pass

sec = r'C:\Users\fazio\OneDrive\Documents\collector\data_provider\binance\candels_1s.json'
days = r'C:\Users\fazio\OneDrive\Documents\collector\data_provider\binance\candels_3d.json'

with open(sec) as jsonfile:
    data_sec = json.loads(jsonfile.read())

with open(days) as jsonfile:
    data_days = json.loads(jsonfile.read())

# this is specific for binance
cand_days = {
    'Kline open time': [el[0] for el in data_days],
    'Open price': [float(el[1]) for el in data_days],
    'High price': [float(el[2]) for el in data_days],
    'Low price': [float(el[3]) for el in data_days],
    'Close price': [float(el[4]) for el in data_days],
    'Volume': [float(el[5]) for el in data_days],
    'Kline close time': [float(el[6]) for el in data_days],
    'Quote asset volume': [float(el[7]) for el in data_days],
    'Number of trades': [float(el[8]) for el in data_days],
    'Taker buy base asset volume': [float(el[9]) for el in data_days],
    'Taker buy quote asset volume': [float(el[10]) for el in data_days],
    'Unused field. Ignore.': [float(el[11]) for el in data_days]
}

for el in cand_days['Kline open time'][:10]:
    print(f"Corresponding date: {datetime.datetime.fromtimestamp(el/1000.0)}",
        "but this doen't work") # I want to get rid of this shit

# Create date range
date_range = pd.date_range(start= datetime.datetime.fromtimestamp(cand_days['Kline open time'][0]/1000.0),
                        end= datetime.datetime.fromtimestamp(cand_days['Kline open time'][-1]/1000.0),
                        periods= len(cand_days['Kline open time']),
                        )


config = dict({'scrollZoom': True,
            'modeBarButtonsToRemove': ['zoom']})

# Create a DataFrame
df = pd.DataFrame({
    'date': date_range,
    'open': cand_days['Open price'],
    'close': cand_days['Close price'],
    'high': cand_days['High price'],
    'low': cand_days['Low price'],
    'volume': cand_days['Volume'],
    'line_data': cand_days['Quote asset volume']
})

print(f"hey !  {df[['date', 'volume']].iloc[10:23]}")

# Create a subplot with 3 rows, 1 column

# Create subplots and mention plot grid size
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.06, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.3, 1.2])

# Plot OHLC on 1st row
fig.add_trace(go.Candlestick(x=df['date'], open=df['open'], high=df['high'],
                low=df['low'], close=df['close'], name="ETHBTC", showlegend= False), 
                row=1, col=1)

# Assuming df is your DataFrame

fig.add_trace(go.Scatter(x=df['date'],
                        y= ((df['open'] + df['close'] + df['high'] + df['low'])/4).rolling(window=7).mean(),
                        mode='lines',
                        line=dict(width=1),
                        name='MA7'), row=1, col=1)

fig.add_trace(go.Scatter(x=df['date'],
                        y= ((df['open'] + df['close'] + df['high'] + df['low'])/4).rolling(window=15).mean(),
                        mode='lines',
                        line=dict(width=1),
                        name='MA15'), row=1, col=1)

fig.add_trace(go.Scatter(x=df['date'],
                        y= ((df['open'] + df['close'] + df['high'] + df['low'])/4).rolling(window=33).mean(),
                        mode='lines',
                        line=dict(width=1),
                        name='MA33'), row=1, col=1)


# Bar trace for volumes on 2nd row without legend
fig.add_trace(go.Bar(x=df['date'], y=df['volume'], showlegend=False), row=2, col=1)

fig.add_trace(go.Scatter(x=df['date'],
                        y= (df['volume']).rolling(window=7).mean(),
                        mode='lines',
                        line=dict(width=1),
                        name='MA7'), row=2, col=1)

fig.add_trace(go.Scatter(x=df['date'],
                        y= (df['volume']).rolling(window=15).mean(),
                        mode='lines',
                        line=dict(width=1),
                        
                        name='MA15'), row=2, col=1)

fig.add_trace(go.Scatter(x=df['date'],
                        y= (df['volume']).rolling(window=33).mean(),
                        mode='lines',
                        line=dict(width=1),
                        name='MA33'), row=2, col=1)

# Do not show OHLC's rangeslider plot 
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show(config=config)