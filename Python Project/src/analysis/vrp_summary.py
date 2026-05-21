"""
3. Variance Risk Premium Summary
Agrégation de la VRP (moyenne et de l'écart-type) globalement et sous contrainte de régimes.
"""

import pandas as pd
import logging
from src.config import PROCESSED_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

def generate_vrp_summary():
    logger.info("--- 3. Generating VRP Summary ---")
    
    input_path = PROCESSED_DIR / "final_analysis_dataset.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Input file introuvable: {input_path}")
        
    df = pd.read_csv(input_path)
    
    # Statistiques globales
    stats = []
    
    # Fonction locale pour extraire et formater une ligne
    def add_stats(regime_name, data_subset):
        if len(data_subset) == 0:
            return
        
        # On calcule std avec degress of freedom = 1 (standard de base pour un sample pandas)
        stats.append({
            "regime": regime_name,
            "mean_btc_vrp_30d": data_subset.get("btc_vrp_30d", pd.Series()).mean(),
            "std_btc_vrp_30d": data_subset.get("btc_vrp_30d", pd.Series()).std(),
            "mean_spx_vrp_30d": data_subset.get("spx_vrp_30d", pd.Series()).mean(),
            "std_spx_vrp_30d": data_subset.get("spx_vrp_30d", pd.Series()).std(),
            "n_obs": len(data_subset)
        })
        
    # Global
    add_stats("All (Global)", df)
    
    # Par régimes
    if "regime_label" in df.columns:
        df_normal = df[df["regime_label"] == "normal"]
        df_stress = df[df["regime_label"] == "stress"]
        
        add_stats("Normal", df_normal)
        add_stats("Stress", df_stress)

    summary_df = pd.DataFrame(stats).round(4)
    
    output_path = OUTPUT_DIR / "vrp_summary.csv"
    summary_df.to_csv(output_path, index=False)
    
    logger.info(f"VRP Summary (Global + Normal/Stress) formaté et sauvegardé : {output_path}")

if __name__ == "__main__":
    generate_vrp_summary()
