"""
Étape 5 : Régressions OLS (IV prédit RV future ?)
Statistiques détaillées avec statsmodels au niveau global et par régime.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import logging
from src.config import PROCESSED_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)

def run_ols(df_subset, x_col, y_col, model_name, hac_lags=30):
    """
    Exécute une régression OLS : y = alpha + beta * x
    avec erreurs-types Newey-West (HAC) pour gérer l'autocorrélation
    induite par le chevauchement des fenêtres roulantes de volatilité.

    hac_lags : nombre de lags Newey-West. Par défaut 30 = horizon de
    la RV future, ce qui couvre la fenêtre de chevauchement.
    """
    # Exclure les NaNs qui résultent du shift et des éventuels trous
    data = df_subset[[x_col, y_col]].dropna()

    n_obs = len(data)
    if n_obs < 10:
        logger.warning(f"Modèle '{model_name}' : pas assez d'observations ({n_obs}).")
        return {
            'Model_Name': model_name, 'Alpha': np.nan, 'Beta': np.nan,
            'T_Stat': np.nan, 'P_Value': np.nan, 'R_Squared': np.nan, 'N_Obs': n_obs
        }

    X = data[x_col]
    Y = data[y_col]
    X_with_const = sm.add_constant(X)

    # HAC (Newey-West) standard errors
    # Justification : RV_{t+h} basée sur une fenêtre roulante de h jours
    # → les résidus successifs partagent jusqu'à h-1 observations,
    # ce qui crée une autocorrélation MA(h-1) mécanique.
    model = sm.OLS(Y, X_with_const).fit(
        cov_type='HAC',
        cov_kwds={'maxlags': hac_lags}
    )

    beta_idx = x_col if x_col in model.params else model.params.index[1]
    const_idx = 'const'

    res = {
        'Model_Name': model_name,
        'Alpha': model.params.get(const_idx, np.nan),
        'Beta': model.params.get(beta_idx, np.nan),
        'Std_Error_HAC': model.bse.get(beta_idx, np.nan),
        'T_Stat_HAC': model.tvalues.get(beta_idx, np.nan),
        'P_Value_HAC': model.pvalues.get(beta_idx, np.nan),
        'R_Squared': model.rsquared,
        'N_Obs': n_obs,
        'HAC_Lags': hac_lags
    }
    return res

def execute_regressions():
    logger.info("--- Exécution des Régressions (IV predict Future RV) ---")
    
    input_path = PROCESSED_DIR / "final_analysis_dataset.csv"
    if not input_path.exists():
        raise FileNotFoundError(f"Le fichier {input_path} n'existe pas. Exécutez l'étape 4.")
        
    df = pd.read_csv(input_path)
    
    # 1. Aligner IV(t) avec RV_future(t+h)
    logger.info("Création des leads (décalage temporel) pour la volatilité future...")
    
    # Création des cibles futures sur les horizons 7, 14, 30
    horizons = [7, 14, 30]
    for h in horizons:
        str_h = str(h)
        df[f'btc_future_rv_{str_h}d'] = df[f'btc_rv_{str_h}d'].shift(-h)
        df[f'spx_future_rv_{str_h}d'] = df[f'spx_rv_{str_h}d'].shift(-h)

    # 2. Séparation par régime
    # Filtres basés sur les colonnes logiques qu'on a créées
    btc_normal_mask = (df['regime_label'] == "normal") # Ou df['btc_stress'] == 0
    btc_stress_mask = (df['btc_stress'] == 1)
    
    spx_normal_mask = (df['regime_label'] == "normal") # Ou df['spx_stress'] == 0
    spx_stress_mask = (df['spx_stress'] == 1)

    # 3. Paramétrage des 6 régressions demandées 
    # Objectif => variable_Y ~ variable_X
    results = []
    
    # Régression 1
    results.append(run_ols(df, 'btc_iv', 'btc_future_rv_30d', '1. Global BTC (RV30 future)'))
    # Régression 2
    results.append(run_ols(df, 'spx_iv', 'spx_future_rv_30d', '2. Global SPX (RV30 future)'))
    
    # Régression 3
    results.append(run_ols(df[btc_normal_mask], 'btc_iv', 'btc_future_rv_30d', '3. BTC Regime Normal'))
    # Régression 4
    results.append(run_ols(df[btc_stress_mask], 'btc_iv', 'btc_future_rv_30d', '4. BTC Regime Stress'))
    
    # Régression 5
    results.append(run_ols(df[spx_normal_mask], 'spx_iv', 'spx_future_rv_30d', '5. SPX Regime Normal'))
    # Régression 6
    results.append(run_ols(df[spx_stress_mask], 'spx_iv', 'spx_future_rv_30d', '6. SPX Regime Stress'))
    
    # 4. Formatage et Sauvegarde
    results_df = pd.DataFrame(results)
    
    output_path = OUTPUT_DIR / "regression_results.csv"
    results_df.to_csv(output_path, index=False)
    
    logger.info(f"Matrice des régressions générée et sauvegardée dans : {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    execute_regressions()
