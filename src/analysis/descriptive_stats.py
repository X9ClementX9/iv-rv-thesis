"""
1. Descriptive Statistics
Construit et exporte la table des statistiques descriptives fondamentales pour la thèse.
"""

import pandas as pd
import logging
from src.config import PROCESSED_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

def generate_descriptive_stats():
    logger.info("--- 1. Generating Descriptive Statistics ---")
    
    input_path = PROCESSED_DIR / "final_analysis_dataset.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Input file introuvable: {input_path}")
        
    df = pd.read_csv(input_path)
    
    target_columns = [
        "btc_rv_30d", "spx_rv_30d", 
        "btc_iv", "spx_iv", 
        "btc_vrp_30d", "spx_vrp_30d"
    ]
    
    # Vérification que les colonnes existent
    available_cols = [c for c in target_columns if c in df.columns]
    data = df[available_cols]
    
    # DataFrame .agg permet de calculer plusieurs métriques d'un coup
    stats = data.agg(['mean', 'std', 'min', 'max', 'skew', 'kurt'])
    
    # Format exigé : une variable par ligne -> transposition de la matrice
    stats = stats.T
    stats = stats.reset_index().rename(columns={"index": "variable"})
    stats = stats.round(4)
    
    output_path = OUTPUT_DIR / "descriptive_stats.csv"
    stats.to_csv(output_path, index=False)
    
    logger.info(f"Descriptive stats (mean, std, min, max, skewness, kurtosis) sauvegardées : {output_path}")

if __name__ == "__main__":
    generate_descriptive_stats()
