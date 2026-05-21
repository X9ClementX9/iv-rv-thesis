import pandas as pd
import requests
import time
from datetime import datetime
from src.config import START_DATE, END_DATE, DATA_DIR, BTC_SYMBOL

def download_btc_spot():
    print(f"--- Téléchargement BTC Spot (Binance) ---")
    url = "https://api.binance.com/api/v3/klines"
    
    start_ts = int(datetime.strptime(START_DATE, "%Y-%m-%d").timestamp() * 1000)
    end_ts = int(datetime.strptime(END_DATE, "%Y-%m-%d").timestamp() * 1000)
    
    all_data = []
    current_ts = start_ts
    
    while current_ts < end_ts:
        params = {
            "symbol": BTC_SYMBOL,
            "interval": "1d",
            "startTime": current_ts,
            "limit": 1000
        }
        res = requests.get(url, params=params)
        data = res.json()
        
        if not data:
            break
            
        all_data.extend(data)
        current_ts = data[-1][6] + 1  # Next start = last close time + 1ms
        time.sleep(0.1) # Respect API limits
        
    df = pd.DataFrame(all_data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'qav', 'num_trades', 'taker_base', 'taker_quote', 'ignore'
    ])
    
    # Cleaning
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['adj_close'] = df['close']
    df['symbol'] = BTC_SYMBOL
    df['source'] = "binance"
    
    df = df[['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'symbol', 'source']]
    df = df[df['date'] <= END_DATE]
    
    output_path = DATA_DIR / "btc_spot_daily_binance.csv"
    df.to_csv(output_path, index=False)
    print(f"Sauvegardé : {output_path}")