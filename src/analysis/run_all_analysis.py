"""
Orchestrateur secondaire : Extraction et analyse statistique empirique de la thèse.
Produit les tables pour les annexes et le texte. (Nécessite la complétion du `Processing` au préalable).
"""
import logging
import sys

# Importation des fonctions de l'analyse
from src.analysis.descriptive_stats import generate_descriptive_stats
from src.analysis.correlations import generate_correlations
from src.analysis.vrp_summary import generate_vrp_summary
from src.analysis.regressions import execute_regressions
from src.analysis.beta_tests import generate_beta_tests
from src.analysis.figures import generate_figures

def main():
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Analyses Statistiques")

    logger.info("=== DEMARRAGE DU PIPELINE STATISTIQUES (ANALYSIS) ===")

    try:
        generate_descriptive_stats()
        generate_correlations()
        generate_vrp_summary()
        execute_regressions()
        generate_beta_tests()
        generate_figures()
        
        logger.info("=== GENERATION STATISTIQUE TERMINEE AVEC SUCCES ===")
        logger.info("Tous les exports finaux de la thèse résident désomais dans le dossier 'data/output/'.")
        
    except Exception as e:
        logger.error(f"Une erreur a mis l'analyse en échec : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
