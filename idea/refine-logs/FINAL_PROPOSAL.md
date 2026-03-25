# Final Proposal: PhyNEO-Polymer — First-Principles Mechanical Property Prediction for Polymers via Bonding-Decomposed MLIP

## Problem Anchor

**Problem**: No machine learning interatomic potential has been used to predict polymer mechanical properties (Young's modulus, stress-strain curves) via atomistic molecular dynamics simulation. All existing approaches either (a) use classical FFs with known 30-50% errors on modulus, or (b) use ML to predict properties directly from molecular structure (no simulation, no physics). This gap prevents computational screening of polymers for applications where mechanical integrity is critical (CO2 capture membranes, battery separators, structural adhesives).

**Scope boundary**: We predict elastic moduli of amorphous polymers below entanglement molecular weight via all-atom MD with PhyNEO-Polymer. We do NOT target: viscoelastic properties, yield/fracture, crystalline polymers, or entangled melts.

---

## Method Thesis

PhyNEO's bonding/non-bonding decomposition — sGNN for intramolecular bonding (torsions, angles, bonds) + physics-driven non-bonding (multipole, Slater, NN correction) — provides a unique advantage for mechanical property prediction: accurate torsional barriers control chain packing, which directly determines elastic modulus. By extending sGNN from electrolyte molecules to diverse polymer repeat units and combining with PhyNEO non-bonding, we enable first-principles-quality mechanical property predictions.

---

## Dominant Contribution

**First demonstration that a bonding-decomposed MLIP (PhyNEO-Polymer) can predict polymer mechanical moduli via MD simulation**, outperforming classical force fields by leveraging DFT-accurate torsional energetics. The causal chain: better torsions → better chain packing → better modulus.

---

## Technical Approach (Refined After Review)

### Architecture: Two-Track Strategy

Given reviewer concern about sGNN-MD scalability (5K-20K atoms needed), we pursue two parallel tracks:

**Track A: Direct sGNN-MD** (preferred if feasible)
- Run full PhyNEO (sGNN bonding + physics non-bonding) in OpenMM via TorchForce
- System size: 5,000-10,000 atoms (below entanglement)
- Target speed: >0.5 ns/day (sufficient for ~5 ns equilibration + 2 ns deformation)
- Existing benchmark: 10K atoms DME tested, 60x GPU speedup with sparse ops

**Track B: sGNN-Informed Classical FF** (fallback)
- Use sGNN to compute high-accuracy torsional profiles for polymer repeat units
- Refit classical FF (OPLS-AA) torsional parameters to match sGNN profiles
- Run large-scale classical MD with improved torsions
- Lower computational cost, same torsional accuracy benefit

### Polymer Selection (5 target systems)

| Polymer | MW (oligomer) | Why | Experimental Modulus |
|---------|--------------|-----|---------------------|
| Polyethylene (PE) | ~2-5 kDa | Simplest, sGNN already trained | ~0.2-1.0 GPa (amorphous) |
| Poly(ethylene oxide) (PEO) | ~2-5 kDa | sGNN already trained, electrolyte relevance | ~0.1-0.5 GPa |
| Poly(methyl methacrylate) (PMMA) | ~3-8 kDa | Stiff backbone, Tg > RT, well-characterized | ~2.4-3.3 GPa |
| Polycarbonate (PC) | ~3-8 kDa | Carbonate group, CO2 relevance | ~2.0-2.4 GPa |
| Nylon-6 (PA6) | ~3-8 kDa | H-bonding, challenging for FFs | ~1.0-2.8 GPa |

### Training Data Generation

1. **Fragment DFT scans**: For each new chemistry (PMMA, PC, PA6), generate torsional scans and conformational energies of dimers-tetramers at ωB97X-D3/def2-TZVP level
2. **Leverage fragment library**: PE and PEO fragments already in PhyNEO training data; C-C, C-O bonds are transferable
3. **New bond types needed**: C=O (ester/carbonate), C-N (amide), aromatic C-C for PC
4. **Estimated DFT cost**: ~500-1000 single-point calculations per new chemistry (~2-4 GPU-hours on A100)

### Mechanical Property Protocol

Following established RadonPy/classical MD protocols:
1. **Build**: Generate amorphous cell (6-10 chains, 5K-10K atoms) via PACKMOL
2. **Equilibrate**: NPT at 300K, 1 atm for 2-5 ns (Track A) or 10-20 ns (Track B)
3. **Deform**: Uniaxial strain at rates 10^8 - 10^10 /s, extract stress-strain
4. **Extract**: Young's modulus from linear regime, Poisson's ratio from lateral strain
5. **Validate**: Compare with experimental values and classical FF predictions

### Ablation Studies

| Experiment | Purpose |
|-----------|---------|
| sGNN + PhyNEO-NB vs OPLS-AA | Full MLIP vs classical FF |
| sGNN + classical NB vs classical FF | Isolate bonding contribution |
| OPLS-AA with sGNN-refit torsions vs original OPLS | Isolate torsion improvement |
| Strain rate convergence | Ensure results are not artifacts |
| System size convergence | 3K vs 5K vs 10K atoms |

---

## Key Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| sGNN-MD too slow for 5K+ atoms | MEDIUM | HIGH | Track B fallback (sGNN-informed classical FF) |
| MD instability (NaN at 100ps) | MEDIUM | HIGH | Debug energy scaling; test with simpler polymers first |
| Modulus improvement < 20% | LOW-MEDIUM | MEDIUM | Even 10% improvement is publishable if systematic; also report Tg, density |
| Non-bonding dominates modulus | LOW | MEDIUM | Ablation will reveal this; adjust narrative accordingly |
| DFT data generation bottleneck | LOW | LOW | Start with PE/PEO (data exists); parallelize DFT jobs |

---

## Expected Outcomes

1. **First MLIP-driven polymer modulus predictions** for 5 polymer systems
2. **Quantified torsion→modulus accuracy cascade**: "X% improvement in torsional accuracy leads to Y% improvement in modulus prediction"
3. **Benchmark**: PhyNEO-Polymer vs OPLS-AA vs GAFF2 vs SimPoly (density/Tg comparison)
4. **Application preview**: CO2-loaded polycarbonate modulus change (if time permits)
5. **Open-source**: Training data, models, and MD protocols released

---

## Paper Positioning

**Target venues**: JCTC (primary), NeurIPS ML4PS workshop, or Nature Computational Science (if results are strong)

**Title options**:
1. "From Torsions to Modulus: First-Principles Polymer Mechanical Properties via Bonding-Decomposed Machine Learning Potential"
2. "PhyNEO-Polymer: Bridging Molecular Accuracy and Macroscopic Mechanical Properties with Physics-Informed Neural Network Potentials"

**Key figures**:
- Fig 1: PhyNEO bonding/non-bonding decomposition schematic for polymers
- Fig 2: Torsional scan comparison (sGNN vs OPLS vs DFT) for 5 polymers
- Fig 3: Stress-strain curves (PhyNEO-Polymer vs classical FF vs experiment)
- Fig 4: Modulus parity plot (predicted vs experimental)
- Fig 5: Ablation — bonding vs non-bonding contribution to modulus accuracy
