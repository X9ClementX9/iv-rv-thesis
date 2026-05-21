"""
Génération des Tableaux PNG prêts à l'emploi (Thèse).
Exporte les CSV vers des images académiques.
"""

import pandas as pd
import dataframe_image as dfi
import logging
from pathlib import Path
from src.config import OUTPUT_DIR, DATA_DIR

logger = logging.getLogger(__name__)

def generate_table_images():
    logger.info("--- Début de la vectorisation des tableaux ---")
    
    # Création du dossier cible pour les images
    IMAGE_DIR = DATA_DIR / "image"
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fonction locale pour uniformiser vos exports
    def export_table(styled_df, filename):
        out_path = IMAGE_DIR / filename
        dfi.export(styled_df, str(out_path), table_conversion="matplotlib", dpi=300)
        logger.info(f"Image générée : {out_path}")

    # ==========================================
    # 1. DESCRIPTIVE STATISTICS
    # ==========================================
    try:
        df_desc = pd.read_csv(OUTPUT_DIR / "descriptive_stats.csv")
        # Format académique (lignes zébrées, header en gras, décimales gérées)
        styled_desc = df_desc.style.set_properties(**{'background-color': '#f8f9fa',
                                                    'color': 'black',
                                                    'border-color': 'white',
                                                    'text-align': 'center'})\
                                  .set_table_styles([{'selector': 'th', 'props': [('background-color', '#343a40'), ('color', 'white'), ('text-align', 'center')]}])\
                                  .hide(axis="index")
        export_table(styled_desc, "table1_descriptive_stats.png")
    except Exception as e:
        logger.warning(f"Impossible de générer Table 1 : {e}")

    # ==========================================
    # 2. CORRELATIONS MATRIX
    # ==========================================
    try:
        df_corr = pd.read_csv(OUTPUT_DIR / "correlation_matrix.csv").set_index('variable')
        styled_corr = df_corr.style.background_gradient(cmap='coolwarm', axis=None, vmin=-1, vmax=1)\
                                   .format(precision=2)
        export_table(styled_corr, "table2_correlation_matrix.png")
    except Exception as e:
        logger.warning(f"Impossible de générer Table 2 : {e}")

    # ==========================================
    # 3. GLOBAL REGRESSIONS (BTC & SPX)
    # ==========================================
    try:
        df_reg = pd.read_csv(OUTPUT_DIR / "regression_results.csv")
        df_global = df_reg[df_reg['Model_Name'].str.contains("Global")].copy()
        
        # Sélection des colonnes demandées par l'utilisateur
        cols = ['Model_Name', 'Alpha', 'Beta', 'Std_Error', 'T_Stat', 'P_Value', 'R_Squared', 'N_Obs']
        df_global = df_global[cols]
        
        styled_global = df_global.style.format({
            "Alpha": "{:.4f}", "Beta": "{:.4f}", "Std_Error": "{:.4f}", 
            "T_Stat": "{:.2f}", "P_Value": "{:.4f}", "R_Squared": "{:.4f}", "N_Obs": "{:,.0f}"
        }).set_table_styles([{'selector': 'th', 'props': [('background-color', '#343a40'), ('color', 'white')]}])\
          .hide(axis="index")
          
        export_table(styled_global, "table3_regression_global.png")
    except Exception as e:
        logger.warning(f"Impossible de générer Table 3 : {e}")

    # ==========================================
    # 4. VRP SUMMARY
    # ==========================================
    try:
        df_vrp = pd.read_csv(OUTPUT_DIR / "vrp_summary.csv")
        styled_vrp = df_vrp.style.format(precision=4)\
                                 .set_table_styles([{'selector': 'th', 'props': [('background-color', '#17a2b8'), ('color', 'white')]}])\
                                 .hide(axis="index")
        export_table(styled_vrp, "table4_vrp_summary.png")
    except Exception as e:
        logger.warning(f"Impossible de générer Table 4 : {e}")

    # ==========================================
    # 5. REGIME SPLIT REGRESSIONS
    # ==========================================
    try:
        df_regime = df_reg[~df_reg['Model_Name'].str.contains("Global")].copy()
        
        # Pour le tableau de régime, on met l'accent sur le beta, on peut enlever Alpha.
        cols_regime = ['Model_Name', 'Beta', 'T_Stat', 'R_Squared', 'N_Obs']
        df_regime = df_regime[cols_regime]
        
        styled_regime = df_regime.style.format({
            "Beta": "{:.4f}", "T_Stat": "{:.2f}", "R_Squared": "{:.4f}", "N_Obs": "{:,.0f}"
        }).set_table_styles([{'selector': 'th', 'props': [('background-color', '#dc3545'), ('color', 'white')]}])\
          .hide(axis="index")
          
        export_table(styled_regime, "table5_regression_regimes.png")
    except Exception as e:
        logger.warning(f"Impossible de générer Table 5 : {e}")

    logger.info("--- Génération des images terminée ---")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s - %(message)s')
    generate_table_images()
