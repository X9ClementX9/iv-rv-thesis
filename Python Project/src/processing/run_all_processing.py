"""
Orchestrateur Principal du Traitement des Données de la Thèse.
Exécute séquentiellement toutes les étapes de la structuration jusqu'à l'analyse économétrique.
"""
import logging
import sys

# Imports des modules du pipeline
from src.processing.build_master_dataset import build_master_dataset
from src.processing.realized_vol import compute_realized_volatility
from src.processing.vrp import compute_vrp
from src.processing.regimes import define_market_regimes
from src.analysis.regressions import execute_regressions

def main():
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Pipeline")
    
    logger.info("=== DEMARRAGE DU PIPELINE DE THÈSE ===")
    
    try:
        # Étape 1
        logger.info("[Etape 1/5] Construction du dataset unifié...")
        build_master_dataset()
        
        # Étape 2
        logger.info("[Etape 2/5] Calcul des volatilités réalisées (RV)...")
        compute_realized_volatility()
        
        # Étape 3
        logger.info("[Etape 3/5] Calcul de la Variance Risk Premium (VRP)...")
        compute_vrp()
        
        # Étape 4
        logger.info("[Etape 4/5] Identification des Régimes de Marché (Stress/Normal)...")
        define_market_regimes()
        
        # Étape 5
        logger.info("[Etape 5/5] Régressions OLS Prédictives...")
        execute_regressions()
        
        logger.info("=== PIPELINE TERMINÉ AVEC SUCCÈS ===")
        logger.info("Tous les résultats d'analyses se trouvent dans le dossier 'data/output/'.")
        
    except Exception as e:
        logger.error(f"Une erreur fatale a arrêté le pipeline : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
