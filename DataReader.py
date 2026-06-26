# implementation of reading data file

# import required modules
import pandas as pd


def read_price_data(
    market_name : str
) -> pd.DataFrame :
    

    file_name = market_name + "_4h.csv"
    
    try:
        price_data = pd.read_csv(
            filepath_or_buffer = f"./Price Data/{file_name}"
        )
    except :

        raise ValueError(
            "invalid market name"
        )
    
    return price_data



if __name__ == "__main__" :

    price_data = read_price_data(
        market_name = "BTC"
    )

    print( price_data )