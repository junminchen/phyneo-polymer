# Experiment Plan: PhyNEO-Polymer Mechanical Property Prediction

## Claim-Driven Experiment Roadmap

Each experiment block directly supports a specific paper claim.

---

## Block 0: Infrastructure Validation (MUST-RUN FIRST)
**Claim**: "sGNN can run MD at polymer-relevant system sizes"

| Run | Description | System | GPU-hours | Success Criterion |
|-----|-------------|--------|-----------|-------------------|
| 0.1 | sGNN speed benchmark at 2K, 5K, 10K atoms | PE oligomers | 1 | >0.5 ns/day at 5K atoms |
| 0.2 | MD stability test (1 ns NPT) | PE 5K atoms | 2 | No NaN, energy drift < 1% |
| 0.3 | OpenMM TorchForce NPT validation | PE 5K atoms | 1 | Density within 5% of experiment |

**Decision gate**: If 0.1 shows <0.1 ns/day at 5K atoms → switch to Track B (sGNN-informed classical FF)

---

## Block 1: Training Data Generation
**Claim**: "PhyNEO-Polymer covers diverse polymer chemistries"

| Run | Description | System | GPU-hours | Output |
|-----|-------------|--------|-----------|--------|
| 1.1 | Torsional scans for PMMA dimers-tetramers | 20 torsion angles × 24 points | 3 | DFT energies + forces |
| 1.2 | Torsional scans for PC dimers-tetramers | 15 torsion angles × 24 points | 2.5 | DFT energies + forces |
| 1.3 | Torsional scans for PA6 dimers-tetramers | 12 torsion angles × 24 points | 2 | DFT energies + forces |
| 1.4 | Conformational sampling (NVT snapshots) for each | 500 configs × 3 polymers | 4 | Training/validation sets |

**Method**: ωB97X-D3/def2-TZVP via Psi4 or ORCA. Use PhyNEO EDA decomposition to separate bonding energies.

---

## Block 2: sGNN Training for New Polymers
**Claim**: "sGNN accurately captures torsional energetics across polymer families"

| Run | Description | System | GPU-hours | Success Criterion |
|-----|-------------|--------|-----------|-------------------|
| 2.1 | Train sGNN for PMMA bond types | PMMA oligomers | 1 | RMSE < 0.05 kcal/mol/atom on test |
| 2.2 | Train sGNN for PC bond types | PC oligomers | 1 | RMSE < 0.05 kcal/mol/atom |
| 2.3 | Train sGNN for PA6 bond types | PA6 oligomers | 1 | RMSE < 0.05 kcal/mol/atom |
| 2.4 | Validate torsional profiles vs DFT | All 5 polymers | 0.5 | Barrier heights within 0.5 kcal/mol |
| 2.5 | Transfer learning test: electrolyte→polymer | PE/PEO (existing) → PMMA | 0.5 | Learning curve comparison |

---

## Block 3: Density and Tg Validation
**Claim**: "PhyNEO-Polymer reproduces bulk thermodynamic properties"

| Run | Description | System | GPU-hours | Success Criterion |
|-----|-------------|--------|-----------|-------------------|
| 3.1 | NPT density at 300K for PE, PEO | 5K atoms each | 4 | Within 3% of experiment |
| 3.2 | NPT density at 300K for PMMA, PC, PA6 | 5K atoms each | 6 | Within 5% of experiment |
| 3.3 | Tg scan (cool from 600K to 100K) | PE, PMMA | 8 | Within 20K of experiment |
| 3.4 | Same runs with OPLS-AA | All 5 polymers | 4 | Baseline comparison |

---

## Block 4: Mechanical Property Prediction (CORE EXPERIMENT)
**Claim**: "PhyNEO-Polymer predicts mechanical moduli more accurately than classical FFs"

| Run | Description | System | GPU-hours | Success Criterion |
|-----|-------------|--------|-----------|-------------------|
| 4.1 | Uniaxial deformation — PE | 5K atoms, 3 replicates × 3 directions | 6 | Modulus within 30% of experiment |
| 4.2 | Uniaxial deformation — PEO | Same protocol | 6 | Same |
| 4.3 | Uniaxial deformation — PMMA | Same protocol | 6 | Same |
| 4.4 | Uniaxial deformation — PC | Same protocol | 6 | Same |
| 4.5 | Uniaxial deformation — PA6 | Same protocol | 6 | Same |
| 4.6 | Same runs with OPLS-AA | All 5 polymers | 10 | Baseline comparison |
| 4.7 | Strain rate convergence test | PMMA at 10^8, 10^9, 10^10 /s | 4 | Identify converged rate |
| 4.8 | System size convergence | PMMA at 3K, 5K, 10K | 6 | Identify minimum size |

**Protocol**:
- Equilibrate: NPT 300K, 1 atm, 2-5 ns
- Deform: constant engineering strain rate, uniaxial along x, y, z
- Extract: σ_xx vs ε_xx, linear fit for E, lateral strain for ν

---

## Block 5: Ablation Studies
**Claim**: "Bonding accuracy (torsions) is the key driver of modulus improvement"

| Run | Description | System | GPU-hours | Purpose |
|-----|-------------|--------|-----------|---------|
| 5.1 | sGNN bonding + OPLS non-bonding | PMMA, PC | 6 | Isolate bonding contribution |
| 5.2 | OPLS bonding + PhyNEO non-bonding | PMMA, PC | 6 | Isolate non-bonding contribution |
| 5.3 | OPLS with sGNN-refit torsions only | PMMA, PC | 4 | Cheapest improvement path |
| 5.4 | Full PhyNEO vs Track B (sGNN-refit OPLS) | PMMA | 4 | Compare direct vs indirect |

---

## Block 6: Application — CO2-Polymer Interaction (STRETCH GOAL)
**Claim**: "PhyNEO-Polymer can predict mechanical changes upon CO2 absorption"

| Run | Description | System | GPU-hours | Success Criterion |
|-----|-------------|--------|-----------|-------------------|
| 6.1 | DFT data: PC + CO2 interactions | 200 configurations | 3 | Training data for CO2-polymer |
| 6.2 | Train sGNN for CO2-polymer bonds | If carbonate forms | 1 | RMSE < 0.05 kcal/mol/atom |
| 6.3 | MD: PC + 0%, 5%, 10% CO2 loading | 5K atoms × 3 loadings | 9 | Density + modulus vs loading |
| 6.4 | Compare with experiment or classical FF | Same systems | 3 | Qualitative trend correct |

---

## Run Order and Dependencies

```
Block 0 (Infrastructure) ──→ DECISION GATE (Track A vs B)
    │
    ├── Track A: Block 1 → Block 2 → Block 3 → Block 4 → Block 5 → Block 6
    │
    └── Track B: Block 1 → Block 2 (torsion refit only) → Block 3 → Block 4 → Block 5 → Block 6
```

**First 3 runs to launch** (Block 0):
1. `0.1` — sGNN speed benchmark (determines Track A vs B)
2. `0.2` — MD stability test (must pass for any MD work)
3. `1.1` — PMMA DFT data generation (can start in parallel)

---

## GPU Budget Summary

| Block | GPU-hours (Track A) | GPU-hours (Track B) |
|-------|-------------------|-------------------|
| 0: Infrastructure | 4 | 4 |
| 1: DFT data | 11.5 | 11.5 |
| 2: Training | 4 | 2 |
| 3: Density/Tg | 22 | 14 |
| 4: Mechanical | 50 | 30 |
| 5: Ablation | 20 | 14 |
| 6: CO2 (stretch) | 16 | 12 |
| **Total** | **~128** | **~88** |

**Estimated wall-clock**: 3-4 weeks (Track A) or 2-3 weeks (Track B) with 2 GPUs.

---

## Success Metrics

| Metric | Minimum for paper | Target |
|--------|------------------|--------|
| Polymers covered | 3 | 5 |
| Modulus MAE vs experiment | < 40% (better than OPLS 50%) | < 25% |
| Torsion RMSE vs DFT | < 0.1 kcal/mol/atom | < 0.05 |
| Density error | < 5% | < 3% |
| Tg error | < 30K | < 20K |
