"""
Étape 4 : Classification des Régimes (Stress vs Normal)
Identifie les extrêmes statistiques historiques (Percentile 90).
"""
import pandas as pd
import numpy as np
import logging
from src.config import PROCESSED_DIR

logger = logging.getLogger(__name__)

def define_market_regimes():
    logger.info("--- Définition des Régimes de Marché ---")
    
    input_path = PROCESSED_DIR / "dataset_with_vrp.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Le fichier {input_path} n'existe pas. Veuillez exécuter l'étape 3.")
        
    df = pd.read_csv(input_path)
    
    # Calcul des percentiles 90 historiques complets
    btc_rv_90p = df['btc_rv_30d'].quantile(0.90)
    # L'utilisateur a explicitement demandé l'indicateur implicite brut pour l'equity
    spx_vix_90p = df['vix_close'].quantile(0.90) 
    
    logger.info(f"Seuil Stress BTC (RV_30d 90th percentile) : {btc_rv_90p:.4f}")
    logger.info(f"Seuil Stress SPX (VIX 90th percentile)   : {spx_vix_90p:.2f}")

    # Génération des colonnes binaires (1 = Stress, 0 = Normal)
    df['btc_stress'] = np.where(df['btc_rv_30d'] > btc_rv_90p, 1, 0)
    df['spx_stress'] = np.where(df['vix_close'] > spx_vix_90p, 1, 0)
    
    # Global Stress (Logique OU)
    df['global_stress'] = np.where((df['btc_stress'] == 1) | (df['spx_stress'] == 1), 1, 0)
    
    # Label textuel
    df['regime_label'] = np.where(df['global_stress'] == 1, "stress", "normal")
    
    # Vérification empirique rapide
    stress_pct = df['global_stress'].mean() * 100
    logger.info(f"Proportion de jours classifiés comme 'stress global' : {stress_pct:.1f}%")

    # Sauvegarde finale du dataset d'analyse
    output_path = PROCESSED_DIR / "final_analysis_dataset.csv"
    df.to_csv(output_path, index=False)
    
    logger.info(f"Dataset d'analyse par régimes prêt et sauvegardé dans : {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    define_market_regimes()
