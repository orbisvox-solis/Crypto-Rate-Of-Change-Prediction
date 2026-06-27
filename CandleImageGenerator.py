# implementation of generating market file candle images in .jpg format

# import required modules
from DataReader import read_price_data
import pandas as pd
import os
import multiprocessing as mp
import numpy as np
import mplfinance as mpf
import matplotlib

matplotlib.use( "Agg" )



def create_dark_style(up_color='#66ff66', down_color='#ff6666'):
    """
    Create a custom mplfinance style with black background and lighter candle colors.
    """
    mc = mpf.make_marketcolors(
        up=up_color,
        down=down_color,
        edge='inherit',        # use same as up/down for candle edges
        wick='inherit',        # use same as up/down for wicks
        volume='inherit',      # use same as up/down for volume bars
        alpha=1.0
    )

    style = mpf.make_mpf_style(
        marketcolors=mc,
        facecolor='black',
        edgecolor='black',
        figcolor='black',
        gridcolor='black',
        gridstyle='',          # no grid lines
        y_on_right=False
    )
    return style

# use plot_window function for ploting specific candle window 
def plot_window(
    # parameters
    symbol : str,
    df_window : pd.DataFrame,
    window_id : int,
    mpl_style ,
    figsize : tuple[int, int] = (6 , 4),
    dpi : int = 80,
    include_volume : bool = False,
    normlized : bool = True,
    padding : float = 0.02,
    y_lim : tuple[float, float] = (-4.0 , 4.0),
    
) -> None:
    
    try:

        if not isinstance( df_window.index , pd.DatetimeIndex ):
            if "time" in df_window.columns : 

                df_window = df_window.set_index( "time" )
            else:

                raise ValueError( "time column is not in df_window")
        
        df_window = df_window.sort_index()

        required_fields = ["open" , "high" , "low" , "close"]

        if not all( col in df_window.columns for col in required_fields ):

            raise ValueError( "your data doesn't have required fields for generating candles image")
        
       
        df_plot = df_window.copy()

        if normlized :

            ohlv_value = df_plot[ required_fields ].values.ravel()

            mean = ohlv_value.mean()
            std = ohlv_value.std()

            if std == 0 :
                std = 1.0
            
            df_plot[ required_fields ] = (
                df_plot[required_fields] - mean
            ) / std

            ylim = y_lim
        
        else:

            pass

        if include_volume == True:
            pass

        else:
            volume = False

        filename = os.path.join( symbol , f"{symbol}_{window_id}.png")


        plot_kwargs = {
            'type': 'candle',
            'volume': volume,
            "style" : mpl_style,
            'title': '',
            'ylabel': '',
            'xlabel': '',
            'axisoff': True,
            'figsize': figsize,
            'tight_layout': True,
            'ylim': ylim,
            'savefig': {
                'fname': filename,
                'dpi': dpi,
                'bbox_inches': 'tight',
                'pad_inches': 0.0,
                'facecolor': 'black'
                },
                'scale_padding': {
                    'left': padding,
                    'right': padding,
                    'top': padding,
                    'bottom': padding
                }
            }

        mpf.plot(
            df_plot,
            **plot_kwargs
        )

        return (symbol, window_id, True, None)
    
    except Exception as e:
        print( e )
        pass

def generate_candle_image(
    market_name : str,
    window_size : int
) -> None :
    

    os.makedirs( market_name , exist_ok = True)
    # read and get data
    price_data = read_price_data(
        market_name = market_name 
    )

    price_data[ "time" ] = pd.to_datetime( price_data["time"] )

    # make style
    style = create_dark_style()

    for index in range( 0 , len( price_data ) - window_size + 1 ):
        plot_window(
            symbol = market_name ,
            df_window = price_data[ index : index + window_size],
            window_id = index ,
            mpl_style = style
        )



if __name__ == "__main__":

    generate_candle_image(
        market_name = "BTC",
        window_size = 7
    )