# Experiment Tracker

| Run ID | Block | Description | Status | GPU-hours Used | Result | Notes |
|--------|-------|-------------|--------|---------------|--------|-------|
| 0.1 | Infra | sGNN speed benchmark 2K/5K/10K | PENDING | — | — | PRIORITY 1 |
| 0.2 | Infra | MD stability test PE 5K 1ns | PENDING | — | — | PRIORITY 1 |
| 0.3 | Infra | OpenMM TorchForce NPT PE | PENDING | — | — | PRIORITY 1 |
| 1.1 | Data | PMMA torsional scans | PENDING | — | — | Can start in parallel |
| 1.2 | Data | PC torsional scans | PENDING | — | — | |
| 1.3 | Data | PA6 torsional scans | PENDING | — | — | |
| 1.4 | Data | Conformational sampling | PENDING | — | — | After 1.1-1.3 |
| 2.1 | Train | sGNN PMMA | PENDING | — | — | After 1.1+1.4 |
| 2.2 | Train | sGNN PC | PENDING | — | — | After 1.2+1.4 |
| 2.3 | Train | sGNN PA6 | PENDING | — | — | After 1.3+1.4 |
| 2.4 | Train | Torsion validation all | PENDING | — | — | After 2.1-2.3 |
| 2.5 | Train | Transfer learning test | PENDING | — | — | After 2.1 |
| 3.1 | Valid | Density PE, PEO | PENDING | — | — | After Block 0 |
| 3.2 | Valid | Density PMMA, PC, PA6 | PENDING | — | — | After Block 2 |
| 3.3 | Valid | Tg scan PE, PMMA | PENDING | — | — | After 3.1, 3.2 |
| 3.4 | Valid | OPLS baseline all | PENDING | — | — | Can start anytime |
| 4.1-4.5 | Mech | Deformation 5 polymers | PENDING | — | — | After Block 3 |
| 4.6 | Mech | OPLS deformation baseline | PENDING | — | — | Can start anytime |
| 4.7 | Mech | Strain rate convergence | PENDING | — | — | After 4.3 |
| 4.8 | Mech | System size convergence | PENDING | — | — | After 4.3 |
| 5.1-5.4 | Ablat | Ablation studies | PENDING | — | — | After Block 4 |
| 6.1-6.4 | CO2 | CO2-polymer stretch goal | PENDING | — | — | After Block 5 |

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| — | Track A vs B | Pending Run 0.1 results |

## Total GPU-hours Budget: 128 (Track A) / 88 (Track B)
## GPU-hours Used: 0
## GPU-hours Remaining: 128 / 88
