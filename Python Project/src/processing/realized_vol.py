"""
Étape 2 : Calcul de la Volatilité Réalisée (RV)
Basé sur les log-returns journaliers et annualisé avec le facteur de la TradFi (252) puisque l'inner join cale le BTC sur le calendrier S&P 500.
"""
import pandas as pd
import numpy as np
import logging
from src.config import PROCESSED_DIR, ANNUALIZATION_FACTOR

logger = logging.getLogger(__name__)

def compute_realized_volatility():
    logger.info("--- Calcul de la Realized Volatility ---")
    
    input_path = PROCESSED_DIR / "master_dataset.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Le fichier {input_path} n'existe pas. Veuillez exécuter l'étape 1.")
        
    df = pd.read_csv(input_path)
    # Assurer le tri chronologique
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    # 1. Calcul des Log Returns
    logger.info("Calcul des Log Returns (BTC & SPX)...")
    df['btc_log_return'] = np.log(df['btc_close'] / df['btc_close'].shift(1))
    df['spx_log_return'] = np.log(df['spx_close'] / df['spx_close'].shift(1))
    
    # 2. Calcul des Rolling Standard Deviations et annualisation
    # Note de méthodologie : L'inner join aligne les jours ouvrés equity. 
    # Mettre np.sqrt(365) pour le BTC fausserait la comparaison car il y a ~252 jours d'observations par an ici.
    horizons = [7, 14, 30]
    
    for h in horizons:
        # std() par defaut dans pandas utilise ddof=1 (sample standard deviation)
        str_h = str(h)
        df[f'btc_rv_{str_h}d'] = df['btc_log_return'].rolling(window=h).std() * np.sqrt(ANNUALIZATION_FACTOR)
        df[f'spx_rv_{str_h}d'] = df['spx_log_return'].rolling(window=h).std() * np.sqrt(ANNUALIZATION_FACTOR)
        logger.info(f"RV {h} jours calculée annotée avec Annualization_Factor={ANNUALIZATION_FACTOR}.")

    # Sauvegarde
    output_path = PROCESSED_DIR / "final_dataset.csv"
    df.to_csv(output_path, index=False)
    
    logger.info(f"Dataset avec RV sauvegardé dans : {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    compute_realized_volatility()
