"""
Étape 3 : Calcul de la Variance Risk Premium (VRP)
VRP = Implied Volatility (IV) - Realized Volatility (RV)
Convertit les indices VIX et DVOL en fractions décimales pour être comparables aux RV.
"""
import pandas as pd
import logging
from src.config import PROCESSED_DIR

logger = logging.getLogger(__name__)

def compute_vrp():
    logger.info("--- Calcul de la Variance Risk Premium (VRP) ---")
    
    input_path = PROCESSED_DIR / "final_dataset.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Le fichier {input_path} n'existe pas. Veuillez exécuter l'étape 2.")
        
    df = pd.read_csv(input_path)
    
    # 1. Extraction et conversion des Implicit Volatility
    # DVOL et VIX sont exprimés en pourcentages (ex: 65.0 pour 65%)
    # On les divise par 100 pour obtenir des valeurs décimales (0.65) et s'aligner mathématiquement sur la RV.
    logger.info("Conversion des indices de volatilité implicite (IV) en décimales...")
    df['btc_iv'] = df['dvol_close'] / 100.0
    df['spx_iv'] = df['vix_close'] / 100.0
    
    # 2. Calcul VRP = IV - RV
    horizons = [7, 14, 30]
    for h in horizons:
        str_h = str(h)
        df[f'btc_vrp_{str_h}d'] = df['btc_iv'] - df[f'btc_rv_{str_h}d']
        df[f'spx_vrp_{str_h}d'] = df['spx_iv'] - df[f'spx_rv_{str_h}d']
        
    # Sauvegarde
    output_path = PROCESSED_DIR / "dataset_with_vrp.csv"
    df.to_csv(output_path, index=False)
    
    logger.info(f"Dataset enrichi de la VRP sauvegardé dans : {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    compute_vrp()
