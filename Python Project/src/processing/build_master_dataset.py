"""
Étape 1 : Construction du Master Dataset.
Fusion des 4 sources de données via Inner Join sur la date pour aligner le BTC sur le calendrier boursier.
"""
import pandas as pd
import logging
from src.config import DATA_DIR, PROCESSED_DIR

logger = logging.getLogger(__name__)

def load_and_prep(filename, prefix):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Fichier manquant : {filepath}")
    
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date']).dt.normalize()
    
    # Selectionner et renommer OHLC(V)
    cols = {'date': 'date'}
    for raw_col in ['open', 'high', 'low', 'close', 'volume']:
        if raw_col in df.columns:
            cols[raw_col] = f"{prefix}_{raw_col}"
            
    df = df[list(cols.keys())]
    df = df.rename(columns=cols)
    return df

def build_master_dataset():
    logger.info("--- Construction du Master Dataset ---")
    
    dfs = {
        'btc': load_and_prep('btc_spot_daily_binance.csv', 'btc'),
        'spx': load_and_prep('spx_daily_yfinance.csv', 'spx'),
        'vix': load_and_prep('vix_daily_yfinance.csv', 'vix'),
        'dvol': load_and_prep('btc_dvol_historical.csv', 'dvol')
    }
    
    # Inner join séquentiel
    master_df = dfs['btc']
    for name in ['spx', 'vix', 'dvol']:
        master_df = pd.merge(master_df, dfs[name], on='date', how='inner')
        
    # Validation du nombre de colonnes et de lignes
    expected_cols = [
        'date', 'btc_open', 'btc_high', 'btc_low', 'btc_close', 'btc_volume',
        'dvol_open', 'dvol_high', 'dvol_low', 'dvol_close',
        'spx_open', 'spx_high', 'spx_low', 'spx_close', 'spx_volume',
        'vix_open', 'vix_high', 'vix_low', 'vix_close'
    ]
    
    # On garantit l'ordre exact demandé par l'utilisateur
    available_cols = [c for c in expected_cols if c in master_df.columns]
    master_df = master_df[available_cols]
    
    # Tri par date par sécurité
    master_df = master_df.sort_values('date').reset_index(drop=True)
    
    output_path = PROCESSED_DIR / "master_dataset.csv"
    master_df.to_csv(output_path, index=False)
    
    logger.info(f"Master Dataset généré : {len(master_df)} jours d'observations communes.")
    logger.info(f"Période: {master_df['date'].min().date()} à {master_df['date'].max().date()}")
    logger.info(f"Sauvegardé dans : {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    build_master_dataset()
