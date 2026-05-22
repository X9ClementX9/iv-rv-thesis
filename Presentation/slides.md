# Defense slides — outline & speaker notes

> Master's thesis defense — *Does implied volatility efficiently predict future realized volatility...*
> Gabin Torres & Clément Massabo — MSc Financial Markets & Investments, SKEMA Business School
> Target: 20 minutes split between two presenters, English, academic style.

---

## Style guide

| Element | Spec |
|---|---|
| Aspect ratio | 16:9 |
| Background | Pure white `#FFFFFF` |
| Primary text | Charcoal `#1F2937` |
| Accent (rule, headlines, key numbers) | Navy `#1F4E79` |
| Secondary accent (subtle, e.g. table headers) | Light grey `#E5E7EB` |
| Title font | Sans-serif: Helvetica Neue / Inter / Arial — bold, 32 pt |
| Body font | Serif: Cambria / EB Garamond / Charter — 18–20 pt |
| Numbers in tables | Tabular figures, 16–18 pt |
| Footer (small, every slide) | "G. Torres & C. Massabo — MSc FMI — May 2025" + slide number, grey 10 pt |

**Visual discipline.** Each slide has a clear hierarchy: one short title (4–6 words), one main idea, one visual or one table or one big number. No more than 30 words of body text on any slide. Speaker notes carry the rest.

---

## Speaker split

- **Speaker 1 (slides 1–7)** — frames the question, the literature, the data and the method. About 10 min. Hand-off at slide 7 on the timeline figure.
- **Speaker 2 (slides 8–15)** — walks through the results, the economic interpretation and closes. About 10 min.

---

## Slide 1 — Cover

**Visible**

> **Does implied volatility efficiently predict future realized volatility,**
> **and how does this relationship vary across market regimes and between**
> **cryptocurrency and equity markets?**
>
> Gabin Torres & Clément Massabo
> Supervisor: Alexandre Landi
> MSc Financial Markets & Investments — SKEMA Business School — May 2025

**Visual**

SKEMA logo top-right (small), navy rule under the title.

**Speaker notes (10 s)**

Speaker 1 introduces both authors, supervisor, and announces the structure: "We'll split the talk in two. I'll cover the question and the method, Clément will walk you through the results and the conclusions."

---

## Slide 2 — The Research Question

**Visible**

> *Big text, centered:*
> **Does implied volatility predict future realized volatility — and is the answer the same for Bitcoin and the S&P 500?**

> *Three small bullets below:*
> - Implied volatility is the market's forecast of future risk.
> - In equities, the relationship has been studied for thirty years.
> - In crypto, it has barely been documented.

**Speaker notes (90 s)**

"Volatility is the central input in derivative pricing, in risk management and in portfolio allocation. Investors and risk managers do not just want to *measure* volatility — they want to *forecast* it. The standard tool for that is implied volatility, extracted from option prices: the VIX in equity markets, DVOL in crypto markets.

The question this thesis asks is whether these indices actually deliver on that promise. In equities we have decades of evidence. In crypto the literature is almost silent. We bring both markets into the same framework and see whether the equity intuitions still hold."

---

## Slide 3 — What We Know vs. What We Don't

**Visible — two columns**

| **Equity markets** | **Crypto markets** |
|---|---|
| IV is informative (Christensen & Prabhala, 1998) | DVOL exists since March 2021 only |
| IV is biased — slope below one, positive premium (Bollerslev, Tauchen, Zhou, 2009) | No comparable predictive evidence |
| Predictive power weakens in crises (Whaley, 2009; Giot, 2005) | No published regime-conditional analysis on BTC options |

**Below**, one line, navy accent:
> *Our contribution: apply the equity benchmark to crypto, in a unified framework, with regime splits.*

**Speaker notes (90 s)**

"On the left, the equity literature is rich and converges on a clear picture: implied volatility carries useful forward-looking information, but it is a biased forecast — the slope of the predictive regression is below one, and the difference is the variance risk premium. It also reacts strongly to stress.

On the right, the crypto side is almost empty. DVOL is the natural analogue of the VIX but it only exists since March 2021. Nobody has, to our knowledge, applied the standard predictive framework to it in a regime-conditional way. That's the gap we close."

---

## Slide 4 — Five Hypotheses

**Visible**

> **H1.** Implied volatility overestimates future realized volatility on average — positive variance risk premium.
> **H2.** Implied volatility is informative but not a perfect predictor.
> **H3.** The variance risk premium is larger in crypto than in equities.
> **H4.** The predictive relationship weakens in stress periods.
> **H5.** Equity markets are close to efficient in normal periods; crypto is not.

**Speaker notes (60 s)**

"Five hypotheses, derived from the equity literature and from the structural features of crypto markets. H1 and H2 are about the level of bias and the predictive power. H3 is the cross-market comparison. H4 and H5 introduce the regime dimension. We test all five empirically and we'll come back to them at the end."

---

## Slide 5 — Data

**Visible — one compact table**

| Series | Provider | Identifier |
|---|---|---|
| Bitcoin spot | Binance public API | `BTCUSDT` daily |
| Bitcoin implied vol. | Deribit public API | `BTC_DVOL` |
| S&P 500 close | Yahoo Finance (`yfinance`) | `^GSPC` |
| VIX close | Yahoo Finance (`yfinance`) | `^VIX` |

> **Period:** 24 March 2021 → 31 December 2025.
> **After NYSE-calendar inner join:** 1 201 daily observations.

**Speaker notes (60 s)**

"Four series, all from public APIs — no proprietary terminal. We align Bitcoin on the NYSE trading calendar so the two markets are observed on the same days. That gives us about 1 200 daily observations from March 2021 to December 2025. The DVOL start date is the binding constraint: it is the youngest series."

---

## Slide 6 — Method, in One Slide

**Visible — four bullets**

> - **Realized volatility:** annualised standard deviation of 30-day log returns.
> - **Predictive regression:** future realized volatility regressed on current implied volatility. *Slope = 1 means efficient.*
> - **Regimes:** *stress* = top 10 % of VIX (equity) or BTC realized volatility (crypto), set ex ante.
> - **Inference:** Newey-West HAC standard errors to correct for rolling-window overlap.

**Speaker notes (90 s)**

"We use the textbook predictive regression: realized volatility over the next 30 days, regressed on the current value of the implied volatility index. The slope tells us how much of the implied volatility signal translates into actual realized volatility. A slope of one would mean perfect efficiency: implied volatility = future realized volatility, no premium.

We then split the sample into normal and stress days, with thresholds fixed ex ante at the 90th percentile of the relevant volatility series. And because realized volatility is built on a rolling window, consecutive observations overlap — we correct standard errors with the Newey-West HAC estimator."

---

## Slide 7 — A First Look (transition)

**Visible**

Large figure centred on the slide: `media/fig_iv_rv_timeline.pdf`.

Below the figure, one line:
> *Red shading marks stress days (90th-percentile thresholds, set ex ante).*

**Speaker notes (90 s)** — *transition slide, Speaker 1 ends, Speaker 2 starts on the same slide*

Speaker 1: "Before getting into the numbers, look at the picture. Top panel, Bitcoin: DVOL in blue, 30-day realized volatility in red. Same for the S&P 500 below. Two things stand out. First, Bitcoin volatility lives in a range four times wider than equity volatility — the level gap is huge. Second, the wedge between implied and realized volatility looks positive on average in both markets, but it doesn't behave the same around stress. I'll let Clément walk you through what those numbers actually say."

*Speaker 2 takes over here.*

---

## Slide 8 — Result 1 · Implied Volatility Is Informative but Biased

**Visible — compact table**

| | **Bitcoin** | **S&P 500** |
|---|---:|---:|
| Slope $\hat\beta$ | **0.55**$^{***}$ | **0.79**$^{***}$ |
| HAC s.e. | (0.09) | (0.10) |
| $R^2$ | 0.33 | 0.36 |
| $H_0: \beta = 1$ | rejected ($p<0.001$) | rejected ($p=0.03$) |
| $N$ | 1 171 | 1 171 |

> *$^{***}$ significant at 1 %. Standard errors are Newey-West HAC, 30 lags.*

**Speaker notes (90 s)**

"Two takeaways. First, both slopes are highly significant and the R-squared is above 0.3, so implied volatility does carry real information. Second, both slopes are also significantly below one. The hypothesis of full efficiency is rejected in both markets. That's the statistical signature of a positive variance risk premium: when implied volatility moves up, realized volatility moves up too, but by less. Investors are paying for something more than a forecast — they are paying for protection."

---

## Slide 9 — The Variance Risk Premium Is Larger in Crypto

**Visible**

> *Two big numbers, side by side, with labels:*

| **Bitcoin** | **S&P 500** |
|:---:|:---:|
| **+0.081** | **+0.035** |
| *avg. variance risk premium* | *avg. variance risk premium* |

> Below: *Crypto investors require more than twice the compensation per unit of volatility risk.* — confirms H3.

**Speaker notes (60 s)**

"Now the variance risk premium directly, market by market. We compute it as implied minus subsequent realized volatility. Both are positive on average, which validates H1. But the crypto premium is more than twice the equity premium. That confirms H3: volatility risk is priced more aggressively in crypto. Higher uncertainty, less standardized hedging, more retail demand for protection — all push the premium up."

---

## Slide 10 — Headline · in Calm Markets, the VIX Looks Almost Efficient

**Visible — minimalist, big number style**

> *Centered, very large, navy:*
> # $\hat\beta = 0.97$
> *S&P 500 — normal regime — $N = 955$*
>
> *Just below, smaller:*
> $p = 0.89$ for $H_0 : \beta = 1$
>
> *Bottom, one line:*
> **We cannot reject that the VIX is a fully efficient predictor in normal periods.**

**Speaker notes (120 s)**

"This is the result I want you to remember. When we restrict the sample to normal-regime days — that's 80 % of the sample — the S&P 500 slope comes back at 0.97, with a HAC standard error of 0.20. We then test the joint efficiency hypothesis β = 1, and we get a p-value of 0.89. That means we cannot reject, at any conventional level, that the VIX is a *fully* efficient predictor of future realized volatility when markets are calm.

This is a strong result. It says that the standard equity literature's pessimism about VIX efficiency comes essentially from stress windows. Outside of those windows, the VIX is, statistically speaking, doing exactly what an efficient option market should do.

In the same regime, Bitcoin's slope stays around 0.54 and the test β = 1 is sharply rejected. So in normal times, equity markets and crypto markets are not in the same league of informational efficiency."

---

## Slide 11 — Original · The Premium Reacts to Stress in Opposite Directions

**Visible — table**

> **Variance risk premium — by regime**

| | **Normal** | **Stress** | **Direction** |
|---|---:|---:|---|
| Bitcoin | +0.087 | **+0.055** | *compresses* |
| S&P 500 | +0.032 | **+0.047** | *widens* |

> Below: *Equity stress widens the premium; crypto stress compresses it.*

**Speaker notes (120 s)**

"And here is the original empirical contribution. When markets enter stress, the variance risk premium does not behave the same way in equities and in crypto. In equities, the premium *widens*: implied volatility rises faster than realized volatility, because demand for protection surges and pushes option prices up before realized volatility has time to materialise. In crypto, the premium *compresses*: realized volatility catches up to and sometimes exceeds DVOL very quickly, because Bitcoin trades 24/7 and the price reacts almost instantly to news.

So a strategy that sells the variance risk premium would behave very differently in the two markets during a crisis. In equities, the premium expands and short-volatility strategies can suffer mark-to-market losses before profiting. In crypto, the premium collapses, and the same strategy faces a different kind of risk. This asymmetry only shows up when both markets are studied side by side."

---

## Slide 12 — Why? Three Economic Mechanisms

**Visible — three rows**

> **1. Hedging demand.** Equity investors buy out-of-the-money puts in stress — pushes the VIX above expected realized volatility.
>
> **2. 24/7 trading.** Bitcoin realized volatility adjusts to news within hours, not days — compresses the wedge faster.
>
> **3. Market maturity.** Equity option markets are deep and dominated by institutions; crypto options are concentrated on a few venues and a more retail base.

**Speaker notes (90 s)**

"Why do we see this asymmetry? Three mechanisms.

First, hedging demand is the standard explanation for the equity-side widening. When risk aversion jumps, institutional investors rush to buy downside protection, and this demand pushes implied volatility above its rational expectation.

Second, the 24/7 nature of crypto trading means realized volatility moves instantaneously when news hits. There's no overnight gap, no weekend pause. So the realized series catches up faster than the implied series can re-price.

Third, the structural difference: equity markets have decades of standardized hedging practices and a deep institutional base. Crypto markets are still concentrated on a handful of venues, with a larger share of retail investors and more leverage. That makes the implied side less stable."

---

## Slide 13 — What We Don't Claim

**Visible — four bullets**

> - **Short sample.** DVOL only goes back to March 2021.
> - **Aggregated indices.** No full option surface — no skew, no term structure.
> - **Daily frequency.** Intraday data would refine realized volatility.
> - **Asymmetric regime definition.** VIX for equity stress vs. realized volatility for crypto stress.

**Speaker notes (60 s)**

"Four caveats worth being upfront about. The DVOL history is short — less than five years. We use aggregated indices, not the full option surface, so we cannot say anything about the skew or the term structure. We work at daily frequency, where intraday data would give finer realized volatility estimates. And we identify stress with different variables across markets — that asymmetry is deliberate but we discuss it openly in the limitations section."

---

## Slide 14 — Take-aways

**Visible — three numbered points**

> **1.** Implied volatility is a **risk-adjusted expectation**, not a raw forecast — in both markets.
>
> **2.** Equity markets are **close to efficient in normal periods**; crypto markets are **not**.
>
> **3.** The variance risk premium **widens in equity stress** and **compresses in crypto stress** — a feature only visible cross-market.
>
> *Code and full dataset:* `github.com/X9ClementX9/iv-rv-thesis`

**Speaker notes (90 s)**

"To wrap up. Three messages.

One, implied volatility — VIX or DVOL — is best interpreted as a risk-adjusted expectation. It carries real information, but it embeds a positive premium that the user has to net out. That's true in both markets.

Two, in calm periods, the VIX is statistically indistinguishable from a fully efficient predictor of equity volatility. DVOL is not — even in calm. So the level of informational efficiency differs sharply between the two option markets, even when the methodology is identical.

Three, in stress, the variance risk premium behaves in opposite ways across the two markets. That asymmetry only shows up when you study both side by side, and it has practical consequences for anyone running volatility strategies across asset classes.

The full dataset and replication code are public on GitHub. The link is on the slide and in the thesis appendix. Thank you."

---

## Slide 15 — Thank You

**Visible**

> *Centered:*
> ## Thank you.
> *Questions?*
>
> *Below, smaller, with a QR code on the right:*
> `github.com/X9ClementX9/iv-rv-thesis`

**Visual**

QR code (right side) pointing to the GitHub repo. A faded version of `fig_iv_rv_timeline.pdf` can be used as background watermark at 10–15 % opacity.

**Speaker notes** — *closing, no speech needed beyond "Thank you, we're happy to take your questions."*

---

## Anticipated Q&A — for your back pocket (no dedicated slide)

| Likely question | Where to look | Short answer |
|---|---|---|
| "Isn't β = 0.97 in normal SPX just low power, not real efficiency?" | Conf. interval on β | "The 95% CI is roughly [0.57, 1.37]. We agree we can't *prove* efficiency, but we can't reject it either. Stronger statement than the global regression." |
| "Why 90th percentile and not 95th?" | Methods | "Trade-off between sample size in the stress regime and how extreme stress has to be. At 95% we'd have ~60 obs in crypto stress, too few. We checked: results are qualitatively similar at 85% and 95%." |
| "Why DVOL and not the full option surface?" | Limitations | "Comparability with VIX, and DVOL is the most complete continuous series available. Term structure and skew analysis is in the future-research section." |
| "Weekends are dropped — bias?" | Data Limitations | "Direction of bias is downward on BTC RV (we drop variance contributions). That works *against* finding a larger crypto VRP — so our H3 result is conservative." |
| "Why HAC and not bootstrap?" | Methods | "HAC is the standard correction for overlapping windows in this literature (Bollerslev-Tauchen-Zhou 2009 use it). Bootstrap would be a robustness check, not a primary tool, given our N." |
| "How would you extend this?" | Future research section | "Ethereum, full surface for term structure, intraday data, regime-switching models, drivers of the premium (macro, sentiment)." |

---

## Delivery tips

- **Rehearse the hand-off at slide 7.** It's the most natural transition point — Speaker 1 finishes on "I'll let Clément walk you through what those numbers actually say." Practice it so it feels seamless.
- **Slides 10 and 11 are the climax.** Slow down. Let the numbers breathe. Pause for two seconds after stating β = 0.97 — let it land.
- **Don't read the slides.** The bullets are reminders for the audience, not your script. The speaker notes here are the script.
- **Have the PDF of the thesis open** on the laptop or in hand — for questions, you'll occasionally want to point to specific tables.
