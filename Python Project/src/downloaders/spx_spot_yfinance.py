import yfinance as yf
import pandas as pd
from src.config import START_DATE, END_DATE, DATA_DIR

def download_yfinance_data(ticker, filename, symbol_name):
    print(f"--- Téléchargement {symbol_name} ({ticker}) via yfinance ---")
    
    # yfinance end_date est exclusive
    end_dt = pd.to_datetime(END_DATE) + pd.Timedelta(days=1)
    
    # On télécharge
    df = yf.download(ticker, start=START_DATE, end=end_dt.strftime('%Y-%m-%d'), interval="1d")
    
    # --- FIX MULTI-INDEX ---
    # Si yfinance renvoie des colonnes de type MultiIndex, on ne garde que le premier niveau (ex: 'Close')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df = df.reset_index()
    
    # Nettoyage des noms de colonnes
    # On s'assure que chaque nom est traité comme une string
    df.columns = [str(c).lower().replace(' ', '_') for c in df.columns]
    
    # Mapping pour coller à ta structure cible
    # yfinance renvoie 'adj_close' ou 'adj_close' selon les versions, on standardise
    if 'adj_close' not in df.columns and 'close' in df.columns:
        df['adj_close'] = df['close']

    df['symbol'] = symbol_name
    df['source'] = "yfinance"
    
    # Sélection et ordre des colonnes (standardisation)
    cols_to_keep = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'symbol', 'source']
    
    # On ne garde que les colonnes qui existent vraiment pour éviter une erreur
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    df = df[existing_cols]
    
    output_path = DATA_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Sauvegardé : {output_path}")