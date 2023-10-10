import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Any, Union, List, Dict, Optional

import pandas as pd



from typing import Any, List, Optional, Callable

class Plot:

    def __init__(self):

        self.config = {'scrollZoom': True,
                       'modeBarButtonsToRemove': ['zoom']}

        self.fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.06, subplot_titles=('OHLC', 'Volume'), 
                    row_width=[0.3, 1.2])

    def __call__(self,
                 indicator_ohlc: Dict[Callable[[pd.DataFrame], Any], Union[List[pd.DataFrame], pd.DataFrame]],
                 df_ohlc: pd.DataFrame,
                 indicator_vol: Optional[List[Callable[[pd.DataFrame], Any]]] = None,
                 volume: Optional[pd.DataFrame] = None) -> Any:

        self.fig.add_trace(go.Candlestick(x=df_ohlc.index, open=df_ohlc['Open'], high=df_ohlc['High'],
                low=df_ohlc['Low'], close=df_ohlc['Close'], name="ETHBTC", showlegend=False), 
                row=1, col=1)
        
        # this can handle only pairs of one indicato and one data
        # it's also unhable to manage plots that rappresents a painted area
        for indicator, params in indicator_ohlc.items():
            self.fig.add_trace(
                              go.Scatter(
                                        x=df_ohlc.index,
                                        y=indicator(params),
                                        mode='lines',
                                        line=dict(width=1),
                                        name=indicator.__name__),
                              row=1,
                              col=1
                              )
        # same as above
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
        
        self.fig.update_layout(xaxis_rangeslider_visible=False,
                            width=1300,
                            height=1000)
        self.fig.show(config=self.config)