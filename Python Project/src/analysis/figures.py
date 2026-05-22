"""
Étape figures : génération des graphiques de la thèse.
Produit deux figures principales :
  fig1 : timeline IV vs RV pour BTC et SPX, zones de stress grisées (2x1)
  fig2 : scatter IV_t vs RV_{t+30} pour les deux marchés avec ligne 45° et regression OLS (1x2)

Exporte dans le dossier media/ du LaTeX (../../../media/) pour que la thèse
les inclue directement.
"""
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from src.config import PROCESSED_DIR

logger = logging.getLogger(__name__)

# Sortie canonique : data/image/ dans le repo (toujours présent quand on clone)
MEDIA_DIR = PROCESSED_DIR.parent / "image"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Sortie optionnelle : dossier media/ de la thèse LaTeX si on travaille en local
# avec le repo cloné. Cible : "<repo>/Thesis/media/".
_THESIS_MEDIA = Path(__file__).resolve().parents[3] / "Thesis" / "media"
THESIS_MEDIA = _THESIS_MEDIA if _THESIS_MEDIA.exists() else None


def _set_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "figure.dpi": 130,
    })


def _shade_stress(ax, dates, mask, color="grey", alpha=0.18):
    """Shade contiguous True regions of mask along dates."""
    if mask.sum() == 0:
        return
    arr = mask.values.astype(int)
    edges = np.diff(np.concatenate(([0], arr, [0])))
    starts = np.where(edges == 1)[0]
    ends = np.where(edges == -1)[0]
    for s, e in zip(starts, ends):
        ax.axvspan(dates.iloc[s], dates.iloc[min(e, len(dates) - 1)],
                   color=color, alpha=alpha, linewidth=0)


def generate_figures():
    logger.info("--- Generation des figures (matplotlib) ---")
    _set_style()

    input_path = PROCESSED_DIR / "final_analysis_dataset.csv"
    df = pd.read_csv(input_path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # ============================================================
    # Figure 1 : timeline IV vs RV avec zones de stress
    # ============================================================
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 5.8), sharex=True)

    # BTC
    ax = axes[0]
    _shade_stress(ax, df["date"], df["btc_stress"] == 1, color="#cc4444")
    ax.plot(df["date"], df["btc_iv"], color="#1f4e79", lw=1.2, label="DVOL (implied)")
    ax.plot(df["date"], df["btc_rv_30d"], color="#c84b16", lw=1.2, label="RV$^{(30)}$ (realized)")
    ax.set_ylabel("Volatility (annualised)")
    ax.set_title("Bitcoin")
    ax.legend(loc="upper right", frameon=False)

    # SPX
    ax = axes[1]
    _shade_stress(ax, df["date"], df["spx_stress"] == 1, color="#cc4444")
    ax.plot(df["date"], df["spx_iv"], color="#1f4e79", lw=1.2, label="VIX (implied)")
    ax.plot(df["date"], df["spx_rv_30d"], color="#c84b16", lw=1.2, label="RV$^{(30)}$ (realized)")
    ax.set_ylabel("Volatility (annualised)")
    ax.set_title("S\\&P 500")
    ax.legend(loc="upper right", frameon=False)

    # X axis formatting
    axes[-1].xaxis.set_major_locator(mdates.YearLocator())
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[-1].set_xlabel("")

    fig.suptitle("Implied vs realized 30-day volatility — stress regimes shaded",
                 fontsize=12, y=1.0)
    fig.tight_layout()
    out1 = MEDIA_DIR / "fig_iv_rv_timeline.pdf"
    fig.savefig(out1, bbox_inches="tight")
    if THESIS_MEDIA:
        fig.savefig(THESIS_MEDIA / "fig_iv_rv_timeline.pdf", bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Figure 1 -> {out1}")

    # --- Variantes 1-panel pour les slides de soutenance ---
    for market, iv_col, rv_col, stress_col, iv_label, title in [
        ("btc", "btc_iv", "btc_rv_30d", "btc_stress", "DVOL (implied)", "Bitcoin"),
        ("spx", "spx_iv", "spx_rv_30d", "spx_stress", "VIX (implied)", "S\\&P 500"),
    ]:
        fig, ax = plt.subplots(figsize=(7.5, 3.4))
        _shade_stress(ax, df["date"], df[stress_col] == 1, color="#cc4444")
        ax.plot(df["date"], df[iv_col], color="#1f4e79", lw=1.3, label=iv_label)
        ax.plot(df["date"], df[rv_col], color="#c84b16", lw=1.3, label="RV$^{(30)}$ (realized)")
        ax.set_ylabel("Volatility (annualised)")
        ax.set_title(title)
        ax.legend(loc="upper right", frameon=False)
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        fig.tight_layout()
        out_single = MEDIA_DIR / f"fig_iv_rv_timeline_{market}.pdf"
        fig.savefig(out_single, bbox_inches="tight")
        if THESIS_MEDIA:
            fig.savefig(THESIS_MEDIA / f"fig_iv_rv_timeline_{market}.pdf", bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Figure 1{market} -> {out_single}")

    # ============================================================
    # Figure 2 : scatter IV_t vs RV_{t+30} avec 45° et OLS line
    # ============================================================
    # Build forward-aligned dataframe
    h = 30
    plot_df = pd.DataFrame({
        "btc_iv": df["btc_iv"],
        "spx_iv": df["spx_iv"],
        "btc_fwd_rv": df["btc_rv_30d"].shift(-h),
        "spx_fwd_rv": df["spx_rv_30d"].shift(-h),
        "btc_stress": df["btc_stress"],
        "spx_stress": df["spx_stress"],
    }).dropna()

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6))

    for ax, market, iv_col, rv_col, stress_col, title in [
        (axes[0], "BTC", "btc_iv", "btc_fwd_rv", "btc_stress", "Bitcoin"),
        (axes[1], "SPX", "spx_iv", "spx_fwd_rv", "spx_stress", "S\\&P 500"),
    ]:
        normal = plot_df[plot_df[stress_col] == 0]
        stress = plot_df[plot_df[stress_col] == 1]

        ax.scatter(normal[iv_col], normal[rv_col], s=8, alpha=0.4,
                   color="#1f4e79", label="Normal", edgecolors="none")
        ax.scatter(stress[iv_col], stress[rv_col], s=10, alpha=0.7,
                   color="#cc4444", label="Stress", edgecolors="none")

        # 45° efficient frontier
        lo = min(plot_df[iv_col].min(), plot_df[rv_col].min()) * 0.95
        hi = max(plot_df[iv_col].max(), plot_df[rv_col].max()) * 1.05
        ax.plot([lo, hi], [lo, hi], color="grey", linestyle=":",
                lw=1.0, label="45$^\\circ$ (efficiency)")

        # OLS line on full sample
        x = plot_df[iv_col].values
        y = plot_df[rv_col].values
        b = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(xs, np.polyval(b, xs), color="black", lw=1.2,
                label=f"OLS: $\\beta$={b[0]:.2f}")

        ax.set_xlabel("Implied volatility $IV_t$")
        ax.set_ylabel("Realized volatility $RV_{t+30}$")
        ax.set_title(title)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.legend(loc="upper left", frameon=False, fontsize=8)

    fig.suptitle("Predictive scatter: $IV_t$ vs $RV^{(30)}_{t+30}$",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    out2 = MEDIA_DIR / "fig_iv_rv_scatter.pdf"
    fig.savefig(out2, bbox_inches="tight")
    if THESIS_MEDIA:
        fig.savefig(THESIS_MEDIA / "fig_iv_rv_scatter.pdf", bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Figure 2 -> {out2}")

    return [out1, out2]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    generate_figures()
