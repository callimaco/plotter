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

from typing import Any, List, Optional, Callable

class Plot:

    def __init__(self):

        self.config = dict({'scrollZoom': True,
            'modeBarButtonsToRemove': ['zoom']})
        
        self.fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.06, subplot_titles=('OHLC', 'Volume'), 
                    row_width=[0.3, 1.2])

    def __call__(self,
                 indicator_ohlc: List[Callable[[pd.DataFrame], Any]],
                 df_ohlc: pd.DataFrame,
                 indicator_vol: Optional[List[Callable[[pd.DataFrame], Any]]] = None,
                 volume: Optional[pd.DataFrame] = None) -> Any:

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
        self.fig.show(config=self.config)