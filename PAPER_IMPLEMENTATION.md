# Paper implementation notes

This repository implements an experimental software-fission and customer-aware
reliability toolkit based on *From Spectral Resilience to Customer Trust: A
Flow–Structural State-Space Theory of Reliability, Customer Experience, and
Stability in Distributed Software Systems* (Anand Sunder, 2026).

Implemented paper-aligned metrics:

- `SRI = 1 - rho(J)`
- `SRIC = (1 - rho(J)) (1 - sigma*)`
- `CIA(t) = ||Hc exp(Jt)||`
- `RSRI = (1 - rho(J))(1 - sigma*) exp(-alpha CIA)`
- normalized customer experience quality (`CEQ`)
- customer reliability as the fraction of observations in the acceptable CEQ region
- trust stability from CEQ variance
- recovery elasticity
- weighted geometric Customer Trust Index (`CTI`)

The formulas are research hypotheses and require calibration against production or
controlled experimental data. The package does not claim that the proposed metrics
are clinically, operationally, or statistically validated.
