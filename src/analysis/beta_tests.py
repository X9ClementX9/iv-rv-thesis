"""
4. Beta Tests (Hypothesis Testing)
Vérifie statistiquement l'homogénéité (H0: Beta = 1) : est-ce que l'IV est un estimateur parfaitement proportionnel de la RV future ?
"""

import pandas as pd
import scipy.stats as stats
import logging
from src.config import OUTPUT_DIR

logger = logging.getLogger(__name__)

def generate_beta_tests():
    logger.info("--- 4. Conduite du test de validité (H0: Beta = 1) ---")
    
    input_path = OUTPUT_DIR / "regression_results.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Input file introuvable: {input_path}")
        
    df = pd.read_csv(input_path)
    
    # On utilise les SE HAC (Newey-West) si disponibles, sinon fallback OLS
    se_col = 'Std_Error_HAC' if 'Std_Error_HAC' in df.columns else 'Std_Error'
    if 'Beta' not in df.columns or se_col not in df.columns:
        raise ValueError(f"L'étape précédente (regressions.py) n'a pas exporté 'Beta' ou '{se_col}'.")

    # t-statistic pour H0: beta = 1 (utilise SE HAC pour cohérence avec les overlapping windows)
    df['T_Stat_Beta_Eq_1'] = (df['Beta'] - 1.0) / df[se_col]
    
    # p-value en bilatéral (two-tailed test) : P(|t_obs| > t)
    # Degrees of freedom (dof) approchés par N - 2 (Beta + Constante = 2 paramètres estimés)
    dof = df['N_Obs'] - 2
    
    # sf = survival function = 1 - cdf
    df['P_Value_Beta_Eq_1'] = stats.t.sf(abs(df['T_Stat_Beta_Eq_1']), dof) * 2
    
    # On ajoute une colonne décisionnelle rapide pour la lecture dans Excel
    # p-value < 0.05 => on rejette H0 (Beta != 1 de manière significative)
    df['Reject_H0_at_5pct'] = df['P_Value_Beta_Eq_1'] < 0.05
    
    # On sélectionne les colonnes intéressantes à exporter spécifiquement
    cols = ['Model_Name', 'Beta', se_col, 'T_Stat_Beta_Eq_1', 'P_Value_Beta_Eq_1', 'Reject_H0_at_5pct']
    beta_tests_df = df[cols].copy()

    # On arrondit
    for c in ['Beta', se_col, 'T_Stat_Beta_Eq_1', 'P_Value_Beta_Eq_1']:
        beta_tests_df[c] = beta_tests_df[c].round(4)
        
    output_path = OUTPUT_DIR / "beta_tests.csv"
    beta_tests_df.to_csv(output_path, index=False)
    
    logger.info(f"Beta=1 Tests complétés : {output_path}")

if __name__ == "__main__":
    generate_beta_tests()
