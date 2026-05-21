"""
2. Correlation Matrix
Génère la matrice des corrélations de Pearson pour valider la relation linéaire entre l'IV, RV et la VRP du BTC et du SPX.
"""

import pandas as pd
import logging
from src.config import PROCESSED_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

def generate_correlations():
    logger.info("--- 2. Generating Correlation Matrix ---")
    
    input_path = PROCESSED_DIR / "final_analysis_dataset.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Input file introuvable: {input_path}")
        
    df = pd.read_csv(input_path)
    
    target_columns = [
        "btc_rv_30d", "spx_rv_30d", 
        "btc_iv", "spx_iv", 
        "btc_vrp_30d", "spx_vrp_30d"
    ]
    
    available_cols = [c for c in target_columns if c in df.columns]
    data = df[available_cols]
    
    # Calcul des corrélations (Pearson par defaut)
    corr_matrix = data.corr().round(4)
    corr_matrix = corr_matrix.reset_index().rename(columns={"index": "variable"})
    
    output_path = OUTPUT_DIR / "correlation_matrix.csv"
    corr_matrix.to_csv(output_path, index=False)
    
    logger.info(f"Matrice de corrélations (Pearson) sauvegardée : {output_path}")

if __name__ == "__main__":
    generate_correlations()
