# Idea Discovery Report

**Direction**: General bonding interaction machine-learning potential for polymer or electrolyte
**Date**: 2026-03-25
**Pipeline**: research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline

---

## Executive Summary

**Recommended idea**: **PhyNEO-Polymer Mechanical Property Prediction** — extend PhyNEO's bonding sGNN to diverse polymer chemistries and demonstrate the first MLIP-driven mechanical property (Young's modulus, stress-strain) prediction via atomistic MD. The key insight is that PhyNEO's bonding/non-bonding decomposition provides DFT-accurate torsional barriers, which control chain packing and directly determine elastic modulus — a causal chain no previous work has demonstrated. Novelty is confirmed (no MLIP has predicted polymer mechanical properties via MD). Reviewer score: 6.5/10 with clear path to improvement via speed benchmarking and ablation studies. Backup idea: CO2-polymer mechanical response screening (7/10 review score, strongest applied impact). Infrastructure assessment shows sGNN scales to 10K atoms on GPU with 60x speedup via sparse ops, with OpenMM TorchForce integration ready. First experiments to launch: sGNN speed benchmark, MD stability test, and PMMA DFT data generation.

**Next step**: Run Block 0 experiments (infrastructure validation) → decide Track A (direct sGNN-MD) vs Track B (sGNN-informed classical FF).

---

## Literature Landscape

See `LITERATURE_SURVEY.md` for full details. Key gaps: (A) No general bonding MLIP for polymers, (B) No MLIP-driven mechanical property prediction, (C) No reactive MLIP for polymer-electrolyte interfaces, (D) No MLIP for polymer-gas mechanical response, (E) Redox stability screening at polymer level.

---

## Brainstormed Ideas (10)

### Idea 1: PolySGNN — Extending PhyNEO's Bonding sGNN to General Polymer Chains

**Description**: Generalize the PhyNEO-Electrolyte sGNN bonding model from small-molecule electrolytes to arbitrary polymer repeat units. The key challenge is handling long chains: the current sGNN uses bond-centric subgraphs with nn=1 (only immediate neighbors). For polymers, we need to capture (a) backbone torsional energetics across multiple repeat units, (b) side-chain conformational coupling, and (c) inter-repeat-unit interactions that are topologically bonded but geometrically distant. The approach: extend the subgraph depth (nn=2 or adaptive), add backbone-aware features (repeat unit index, backbone vs side-chain flag), and train on polymer oligomer conformational energies from DFT.

**Hypothesis**: A bonding-aware sGNN trained on oligomer DFT data with extended subgraph depth will predict polymer conformational energies and torsional barriers more accurately than classical FFs (OPLS-AA, GAFF2) while being 100-1000x faster than AIMD.

**Key Technical Approach**:
- Extend sGNN subgraph depth from nn=1 to nn=2 for backbone bonds
- Add repeat-unit-aware features (position along backbone, branch type)
- Train on DFT conformational scans of oligomers (dimers through hexamers) for 20-30 common polymer chemistries
- Combine with PhyNEO non-bonding for full potential
- Validate on polymer density, Tg, and conformational distributions vs SimPoly and experiment

**Expected Impact**: HIGH — enables first-principles-quality polymer simulations with PhyNEO's physics-informed decomposition
**Feasibility**: HIGH — sGNN code exists, mainly needs training data generation and architectural extension
**Compute Cost**: ~4-8 GPU-hours for pilot (DFT data generation is the bottleneck, but can start with 2-3 polymers)
**Novelty**: SimPoly uses end-to-end MLFF without decomposition. PhyNEO only covers electrolyte molecules. This would be the first bonding/non-bonding decomposed MLIP for polymers. Closest: SimPoly (no decomposition), PhyNEO (no polymers).

---

### Idea 2: Mechanical Property Prediction via MLIP-Driven Polymer MD

**Description**: Use an MLIP (PolySGNN or fine-tuned foundation model) to run large-scale polymer MD simulations and directly predict mechanical properties — Young's modulus, bulk modulus, Poisson's ratio, and stress-strain curves — from first principles. No existing work does this: all ML mechanical property predictions are structure→property mappings (no simulation), while all MD mechanical simulations use classical FFs. The key insight: mechanical properties depend sensitively on non-bonded interactions, torsional barriers, and chain packing — all areas where classical FFs are weak and MLIPs could shine.

**Hypothesis**: MLIP-driven MD will predict polymer mechanical moduli within 15% of experiment, outperforming OPLS-AA/GAFF2 (which typically have 30-50% errors on modulus).

**Key Technical Approach**:
- Build PolySGNN (Idea 1) or fine-tune MACE/Vivace for target polymers
- Run NPT equilibration → uniaxial deformation MD at MLIP accuracy
- Extract stress-strain curve, Young's modulus, yield point
- Benchmark against experiment and classical FF results for 5-10 well-characterized polymers (PE, PP, PET, PMMA, Nylon-6)
- Key challenge: system size (need ~5000-10000 atoms for mechanical properties) and timescale (ns-scale deformation)

**Expected Impact**: HIGH — first demonstration of MLIP-quality mechanical property prediction for polymers
**Feasibility**: MEDIUM — requires PolySGNN to work first, plus large-scale MD infrastructure
**Compute Cost**: ~8-20 GPU-hours for pilot (one polymer, one deformation direction)
**Novelty**: No prior work. Closest: SimPoly (density/Tg only), classical FF mechanical simulations.

---

### Idea 3: CO2-Polymer Interaction MLIP for Carbon Capture Membrane Screening

**Description**: Develop an MLIP that captures how CO2 absorption changes the mechanical properties of polymers used in carbon capture membranes. Experimentalists report that carbonate incorporation can dramatically change polymer stiffness, but no computational method predicts this accurately. The approach: train a bonding MLIP on polymer + CO2/carbonate systems, then run MD to measure (a) CO2 solubility, (b) diffusivity, (c) modulus change as a function of CO2 loading. This directly answers the experimentalists' question: "which polymers maintain structural integrity under CO2 loading?"

**Hypothesis**: An MLIP trained on polymer-CO2 interaction DFT data will predict the modulus reduction upon CO2 absorption within 20% of experiment, enabling computational screening of CO2-resistant polymer membranes.

**Key Technical Approach**:
- Generate DFT data: polymer oligomer + CO2 configurations (adsorption geometries, carbonate formation)
- Train PolySGNN bonding model for polymer-CO2 bonded interactions + PhyNEO non-bonding for polymer...CO2 van der Waals
- Run MD at various CO2 loadings: measure density, modulus, gas diffusivity
- Screen 10-20 candidate polymers (PIMs, PBI, polyimides, polycarbonates)
- Identify polymers unsuited for scalable CO2 capture processes (excessive softening)

**Expected Impact**: HIGH — directly addresses experimentalist needs, potential for high-impact applied paper
**Feasibility**: MEDIUM — requires DFT data for polymer-CO2 systems, which is tractable but requires careful setup
**Compute Cost**: ~6-12 GPU-hours for pilot (one polymer + CO2)
**Novelty**: No existing MLIP study on CO2-polymer mechanical response. Closest: classical FF CO2 diffusion in PIMs (no mechanical properties), ML screening of MOFs for CO2 (not polymers).

---

### Idea 4: Torsion-Entropy-Aware MLIP for Polymer Reaction Pathway Prediction

**Description**: Build an MLIP that accurately captures torsional energy landscapes of polymer monomers and oligomers, enabling quantitative prediction of (a) polymerization reaction pathways and (b) conformational entropy contributions to reaction free energies. Current classical FFs systematically overestimate torsional barriers (OPLS issue), leading to wrong entropy predictions. The approach: use the sGNN dihedral features (already in the codebase: 9 dihedral features per bond) as the foundation, train on high-accuracy torsional scans (CCSD(T) or DFT-D4), and compute free energy surfaces via enhanced sampling (metadynamics or replica exchange).

**Hypothesis**: An sGNN trained on high-accuracy torsional scans will predict conformational free energies within 0.5 kcal/mol of CCSD(T), enabling qualitative explanation of experimentally observed polymerization selectivities through torsion entropy.

**Key Technical Approach**:
- Generate torsional scan DFT data for 15-20 common monomers (acrylates, styrenes, vinyl ethers, etc.)
- Train sGNN with emphasis on dihedral feature accuracy (possibly increase dihedral feature count beyond 9)
- Run well-tempered metadynamics on oligomers to compute free energy landscapes
- Compare predicted conformational preferences and reaction barriers with experiment
- Identify monomers where torsion entropy drives selectivity

**Expected Impact**: MEDIUM-HIGH — provides mechanistic insight that experimentalists value
**Feasibility**: HIGH — sGNN already has dihedral features, just needs better training data
**Compute Cost**: ~2-4 GPU-hours for pilot (torsional scans + short metadynamics for 2-3 monomers)
**Novelty**: QRNN corrects OPLS torsions but doesn't connect to reaction pathways or entropy. No MLIP study links torsion accuracy to polymerization selectivity. Closest: QRNN torsion correction (no reaction pathways).

---

### Idea 5: Redox-Stability-Informed MLIP for Li-S Battery Polymer Separator Screening

**Description**: Combine MLIP-driven conformational sampling with redox potential prediction to screen polymer membranes for Li-S battery separators. Current approaches use monomer-level DFT for redox potentials, ignoring conformational effects. The key insight: the redox potential of a polymer depends on its conformation (which affects HOMO/LUMO energies), and conformational sampling with an accurate MLIP can provide ensemble-averaged redox potentials that are more predictive than single-point monomer calculations.

**Hypothesis**: Ensemble-averaged redox potentials from MLIP-sampled polymer conformations will correlate better with experimental electrochemical stability windows (R² > 0.8) than single-monomer DFT calculations (R² ~ 0.5-0.6).

**Key Technical Approach**:
- Train PolySGNN for candidate separator polymer chemistries (PEO, PVDF, PAN, PBI, sulfonated polyimides)
- Run MLIP MD to generate equilibrium conformational ensembles
- Compute redox potentials on sampled snapshots via DFT (HOMO/LUMO from ωB97X-D) — "ML-accelerated sampling + DFT single-points"
- Build a mapping: polymer chemistry → conformational ensemble → redox stability window
- Screen 30+ polymers and rank by electrochemical stability

**Expected Impact**: MEDIUM-HIGH — practical tool for battery materials screening
**Feasibility**: MEDIUM — requires both MLIP training and DFT single-point infrastructure
**Compute Cost**: ~4-8 GPU-hours for pilot (2-3 polymers, MLIP training + DFT single points)
**Novelty**: No prior work combines MLIP conformational sampling with redox potential prediction for polymer screening. Closest: monomer DFT screening (no conformational effects), ML redox potential from molecular graphs (no physics-based sampling).

---

### Idea 6: Reactive Bonding MLIP for Polymer Degradation and Crosslinking

**Description**: Extend the sGNN bonding model to handle bond breaking and formation during polymer degradation, crosslinking, or curing. The current sGNN uses fixed topology (bonds defined at initialization). The extension: (a) use distance-based bond detection with hysteresis, (b) dynamically rebuild subgraphs when bonds form/break, (c) train on DFT trajectories that include reactive events. Target systems: epoxy curing (crosslinking), PEO degradation at Li electrode, polymer chain scission under mechanical stress.

**Hypothesis**: A reactive sGNN with dynamic topology will reproduce bond-breaking energetics within 2 kcal/mol of DFT while being 500x faster than AIMD, enabling simulation of polymer degradation at experimentally relevant timescales.

**Key Technical Approach**:
- Modify graph.py to support dynamic bond detection (distance + history based)
- Train on AIMD trajectories of reactive events (bond breaking/formation)
- Use physics-constrained data augmentation (Morse potential for dissociation curves)
- Validate on crosslinking degree vs cure time for epoxy systems
- Compare with existing reactive MLFF for crosslinked epoxy

**Expected Impact**: HIGH — enables new class of polymer simulations
**Feasibility**: LOW-MEDIUM — significant code changes to sGNN, need reactive DFT data
**Compute Cost**: ~8-16 GPU-hours for pilot (AIMD reactive trajectories are expensive)
**Novelty**: Reactive MLFF for epoxy exists but doesn't use bonding/non-bonding decomposition. Reactive sGNN with PhyNEO physics would be novel. Closest: reactive MLFF for crosslinked epoxy (no decomposition).

---

### Idea 7: Transfer Learning from Electrolyte sGNN to Polymer sGNN

**Description**: Instead of training polymer sGNN from scratch, use transfer learning from the existing PhyNEO-Electrolyte sGNN models. The insight: bonded interactions are local and transferable — a C-C bond in DMC behaves similarly to a C-C bond in polyethylene. Pre-train on electrolyte monomer data (already available), then fine-tune on small polymer oligomer datasets. This could dramatically reduce the data requirement for polymer MLIP development.

**Hypothesis**: Transfer learning from electrolyte sGNN to polymer sGNN will achieve 80% of from-scratch accuracy with only 20% of the training data, enabling rapid extension to new polymer chemistries.

**Key Technical Approach**:
- Freeze lower sGNN layers (feature extraction) trained on electrolyte data
- Fine-tune upper layers (readout) on polymer oligomer DFT data
- Systematically test: how much polymer data is needed for convergence?
- Compare learning curves: transfer vs from-scratch
- Extend to 5-10 polymer families to test transferability

**Expected Impact**: MEDIUM — methodological contribution to data-efficient MLIP training
**Feasibility**: HIGH — minimal code changes, uses existing trained models
**Compute Cost**: ~2-4 GPU-hours for pilot
**Novelty**: Transfer learning for MLIPs exists but not from electrolyte→polymer in a bonding-decomposed framework. Closest: foundation model fine-tuning (MACE-MP-0, but not bonding-specific).

---

### Idea 8: Multi-Scale Bonding MLIP: From Monomer Torsions to Polymer Modulus

**Description**: Build a unified multi-scale framework that connects monomer-level torsional accuracy (from sGNN) to macroscopic mechanical properties (from large-scale MD). The pipeline: (1) sGNN provides accurate monomer/oligomer torsional energetics, (2) these are used to parameterize a coarse-grained model or run direct all-atom MD, (3) mechanical properties emerge from the simulation. The key contribution: demonstrating a causal chain from first-principles torsion accuracy to macroscopic modulus prediction, validating that MLIP improvements at the monomer level propagate to improved mechanical predictions.

**Hypothesis**: Improving torsional accuracy from OPLS-level to DFT-level via sGNN will improve mechanical modulus predictions by >20% for flexible polymers where torsional barriers control chain packing.

**Key Technical Approach**:
- Compare sGNN vs OPLS torsional scans for 5 representative polymers
- Run all-atom MD with both sGNN and OPLS for density, Rg, persistence length
- Run deformation MD for modulus with both potentials
- Quantify: how much does torsion accuracy improvement translate to modulus improvement?
- Identify polymer classes where torsion accuracy matters most

**Expected Impact**: MEDIUM-HIGH — demonstrates the value proposition of MLIP for polymer engineering
**Feasibility**: MEDIUM — requires full MLIP MD infrastructure + deformation protocols
**Compute Cost**: ~6-10 GPU-hours for pilot
**Novelty**: No prior work demonstrates the torsion→modulus accuracy cascade for MLIPs. Closest: SimPoly (density/Tg only), classical FF modulus studies.

---

### Idea 9: PhyNEO-Polymer: Full Bonding + Non-Bonding MLIP with Long-Range Electrostatics for Polymer Electrolytes

**Description**: Combine the PhyNEO bonding sGNN (extended for polymers, Idea 1) with the PhyNEO non-bonding framework (multipole + Slater + NN) AND add a long-range electrostatic treatment (charge equilibration or Ewald) to build a complete MLIP for polymer electrolyte systems (e.g., PEO-LiTFSI). This addresses the full problem: bonded interactions along the polymer chain, short-range non-bonding between polymer segments, and long-range electrostatics for ion transport.

**Hypothesis**: A full PhyNEO-Polymer potential with explicit long-range electrostatics will predict Li+ diffusivity in PEO-LiTFSI within 0.5 order of magnitude of experiment, outperforming both classical FFs (which get the wrong mechanism) and short-range-only MLIPs (which miss electrostatic effects).

**Key Technical Approach**:
- Extend sGNN for PEO backbone (Idea 1)
- Use existing PhyNEO non-bonding for PEO...Li+, PEO...TFSI- interactions
- Add charge equilibration (from QRNN or PhyNEO polarization model)
- Train on AIMD trajectories of PEO-LiTFSI at various salt concentrations
- Validate: ionic conductivity, Li+ coordination, diffusivity

**Expected Impact**: VERY HIGH — complete first-principles polymer electrolyte potential
**Feasibility**: LOW-MEDIUM — requires integrating multiple PhyNEO components + long-range treatment
**Compute Cost**: ~10-20 GPU-hours for pilot
**Novelty**: No complete bonding+non-bonding+long-range MLIP for polymer electrolytes exists. Closest: PhyNEO-Electrolyte (small molecules only), end-to-end classical potential fitting (Chemistry of Materials 2025, no ML bonding).

---

### Idea 10: Polymer Chemistry Space Exploration via Few-Shot sGNN Adaptation

**Description**: Develop a few-shot learning strategy for rapidly adapting the sGNN to new polymer chemistries with minimal DFT data. The idea: since sGNN operates on bond-centric subgraphs and most bonds are transferable across chemistries (C-C, C-O, C-N, C=O, etc.), a new polymer only requires training data for its *unique* bond types or combinations. Build a "bond type library" and a meta-learning protocol that identifies which bond types need new data and generates only those conformations.

**Hypothesis**: A meta-learned sGNN with bond-type decomposition can adapt to a new polymer chemistry with only 50-100 DFT calculations (vs 1000+ for training from scratch), enabling high-throughput polymer screening.

**Key Technical Approach**:
- Catalog all unique bond types in sGNN across polymer families
- Build a bond-type energy library from existing training data
- For new polymer: identify novel bond-type combinations, generate targeted DFT data
- Fine-tune only the subgraphs involving novel bond types
- Benchmark: adaptation quality vs data quantity for 10 diverse polymers

**Expected Impact**: MEDIUM-HIGH — enables high-throughput MLIP-quality polymer screening
**Feasibility**: HIGH — leverages bond-centric design of sGNN naturally
**Compute Cost**: ~2-4 GPU-hours for pilot
**Novelty**: Few-shot MLIP adaptation exists for materials (via foundation models) but not exploiting bond-type decomposition. Closest: MACE-MP-0 fine-tuning (not bond-aware).

---

## Phase 3: Deep Novelty Verification Results

### Critical Finding: sGNN already demonstrated on polymers

The original PhyNEO/sGNN paper (JPCL 2021, arXiv:2106.00927) and PhyNEO JCTC 2023 already demonstrated:
- sGNN trained on PEG[2] and PEG[4], tested on PEG[4] and PEG[8]
- RMSE 0.020 kcal/mol/atom, outperforming OPLS-AA and TensorMol
- Also tested on polyethylene and PEG-PE block copolymers
- Linear scaling with system size (one subgraph per bond)
- "Fragment library" concept: train on small fragments, predict large polymers

**Implication**: Idea 1 (PolySGNN) as stated is NOT novel. The basic sGNN→polymer extension is published by the same group. Ideas must be reframed around what's NEW beyond PEG/PE.

### Novelty Assessment per Idea (Updated)

| # | Idea | Novelty Status | Closest Work | Differentiation |
|---|------|---------------|-------------|-----------------|
| 1 | PolySGNN | PARTIALLY PUBLISHED | PhyNEO JPCL 2021 (PEG/PE) | Novel if extended to diverse chemistries (20+ families) |
| 2 | Mechanical Properties via MLIP MD | **CONFIRMED NOVEL** | Universal MLIP modulus (MOFs only, arXiv:2511.22885); SimPoly (density/Tg only) | First MLIP-driven stress-strain for polymers |
| 3 | CO2-Polymer Mechanical | **CONFIRMED NOVEL** | Classical FF CO2 diffusion in PIMs; ML MOF screening for CO2 | First MLIP for CO2-induced mechanical changes in polymers |
| 4 | Torsion-Entropy Pathways | **CONFIRMED NOVEL** | QRNN torsion corrections; entropy-driven ROMP (JACS) | First to link MLIP torsion accuracy → polymerization selectivity |
| 5 | Redox Li-S Screening | PARTIALLY NOVEL | MLP redox via TI (JACS 2024, small molecules) | Novel for polymer membranes with conformational sampling |
| 6 | Reactive Bonding | PARTIALLY NOVEL | Reactive MLFF for epoxy (2025) | Novel with bonding/non-bonding decomposition |
| 7 | Transfer Learning | LOW NOVELTY | Fragment library already in PhyNEO paper | Incremental over existing approach |
| 8 | Torsion→Modulus | **CONFIRMED NOVEL** | No prior work connecting these | Compelling causal chain demonstration |
| 9 | Full PhyNEO-Polymer | NOVEL but large scope | No complete system exists | Better as long-term project |
| 10 | Few-Shot Adaptation | MEDIUM NOVELTY | Foundation model fine-tuning exists | Bond-type decomposition angle is new |

### Re-Ranked Ideas (Post-Novelty)

| Rank | Idea | Impact × Feasibility × Novelty | Status |
|------|------|-------------------------------|--------|
| 1 | **Idea 2+8 Combined**: MLIP Mechanical Properties (Torsion→Modulus) | VERY HIGH | TOP PICK |
| 2 | **Idea 3**: CO2-Polymer Mechanical Response | HIGH | STRONG BACKUP |
| 3 | **Idea 4**: Torsion-Entropy for Reaction Pathways | MED-HIGH | BACKUP |
| 4 | **Idea 5**: Redox Li-S Screening | MEDIUM | EXPLORATORY |
| 5 | **Idea 1 (reframed)**: PolySGNN for 20+ diverse chemistries | MEDIUM | FOUNDATIONAL |

### Recommended Top Idea: PhyNEO-Polymer Mechanical Property Prediction

**Combined Idea 2+8**: Use PhyNEO's bonding sGNN (extended to diverse polymers) to predict mechanical properties via MD simulation, demonstrating that first-principles torsional accuracy propagates to macroscopic modulus predictions.

**Why this is the strongest:**
1. **Clear novelty**: No MLIP has predicted polymer mechanical properties via MD (universal MLIPs only tested on MOFs/inorganics)
2. **High impact**: Experimentalists urgently need this (CO2 capture, battery membranes)
3. **Feasible**: sGNN code exists and already works for PEG/PE; needs extension to more chemistries + deformation protocol
4. **Publishable story**: "We show that improving torsional accuracy from classical FF to DFT-level via sGNN improves mechanical modulus predictions by X%, enabling first-principles polymer engineering"
5. **Natural follow-up**: CO2-polymer (Idea 3) and redox screening (Idea 5) become applications of the same framework

---

## Phase 4: External Critical Review

### Review of Top Idea: PhyNEO-Polymer Mechanical Property Prediction

**Reviewer: Senior ML-for-Science Reviewer (NeurIPS/ICML level)**

#### Summary
The proposal extends PhyNEO's sGNN bonding model to diverse polymer chemistries and uses it for first-principles mechanical property prediction (modulus, stress-strain) via MD simulation. The key claim is that improving torsional accuracy at the monomer level propagates to better macroscopic mechanical predictions.

#### Strengths
1. **Clear gap**: No existing MLIP has predicted polymer mechanical properties via atomistic MD. Universal MLIPs (MACE-MP-0, Orb-v3) were only tested on MOFs/inorganics for modulus. SimPoly stops at density/Tg. This would be genuinely first.
2. **Strong existing codebase**: sGNN already works for PEG/PE with excellent accuracy (0.020 kcal/mol/atom). Extension to more chemistries is feasible.
3. **Practical impact**: Experimentalists in CO2 capture and battery membrane communities need computational mechanical property predictions. Classical FFs have 30-50% errors.
4. **Clean narrative**: Torsion accuracy → chain packing → modulus. Testable causal chain.

#### Weaknesses
1. **System size bottleneck (MAJOR)**: Mechanical property prediction requires 5,000-20,000 atoms and ns-timescale deformation. sGNN runs on JAX with vmapped subgraph evaluations — unclear if it scales to 20K atoms within reasonable wall-clock time. Classical FFs handle this easily; MLIP overhead could make it prohibitively slow.
   - *Mitigation*: Benchmark sGNN speed per step vs classical FF. If too slow, use sGNN to reparametrize a classical FF (indirect approach) rather than running sGNN-MD directly.

2. **Entanglement timescale (MAJOR)**: Mechanical properties of high-MW polymers depend on chain entanglement, which requires >100 ns equilibration. Even with fast sGNN, this may need coarse-graining or enhanced sampling.
   - *Mitigation*: Start with short-chain oligomers (below entanglement MW) where chain packing dominates. Still meaningful for many applications (coatings, membranes).

3. **DFT training data scope (MODERATE)**: Extending to 20+ polymer chemistries requires significant DFT data generation. The "fragment library" concept from PhyNEO helps, but validation across diverse chemistries is labor-intensive.
   - *Mitigation*: Start with 5 well-characterized polymers (PE, PEO, PMMA, Nylon-6, polycarbonate) where experimental modulus data exists for validation.

4. **Non-bonding contribution to modulus (MODERATE)**: Mechanical properties depend heavily on van der Waals packing and potentially hydrogen bonding, not just torsional accuracy. The sGNN only handles bonding — the non-bonding side (PhyNEO multipole + Slater + NN) must also be accurate for the full system.
   - *Mitigation*: Use full PhyNEO (bonding + non-bonding) for the demonstration. Ablation: sGNN + classical non-bonding vs full PhyNEO to isolate bonding contribution.

5. **Comparison fairness (MINOR)**: Comparing MLIP modulus vs classical FF modulus is only meaningful if both use the same equilibration protocol, system size, and strain rate. Strain-rate effects are large in MD.
   - *Mitigation*: Follow established protocols (e.g., RadonPy workflow) with systematic strain-rate convergence tests.

#### Missing Experiments
- Speed benchmark: sGNN atoms/step/second at 5K, 10K, 20K atoms
- Strain-rate sensitivity analysis
- Ablation: bonding-only sGNN vs full PhyNEO vs classical FF
- Cross-validation: train on oligomers, test on longer chains

#### Score: 6.5/10

**Verdict**: Strong novelty and practical value, but significant computational feasibility concerns. The paper would be ACCEPT if: (a) sGNN-MD is shown to be fast enough for 5K+ atom systems, or (b) the authors use sGNN to improve classical FF torsional parameters (indirect approach) and show modulus improvement, or (c) the scope is narrowed to oligomeric systems below entanglement.

#### Minimum Viable Improvements
1. Run sGNN speed benchmark at polymer-relevant system sizes (5K-20K atoms)
2. If direct sGNN-MD is too slow, pivot to "sGNN-informed classical FF" approach
3. Include non-bonding ablation to isolate bonding contribution to modulus
4. Start with 5 polymers with well-known experimental moduli for clean validation

---

### Review of Backup Idea: CO2-Polymer Mechanical Response (Idea 3)

#### Score: 7/10

**Verdict**: Even stronger applied impact than the top idea. The question "how does CO2 absorption change polymer modulus?" is directly actionable for experimentalists. Novelty is confirmed. Main risk: requires both polymer MLIP AND polymer-CO2 interaction training, doubling the data generation effort.

**Recommendation**: Position Idea 3 as the APPLICATION demonstration of the framework from Idea 2+8. Train PhyNEO-Polymer → demonstrate on mechanical properties → apply to CO2 loading as the killer application.

---

### Review of Backup Idea: Torsion-Entropy for Reaction Pathways (Idea 4)

#### Score: 6/10

**Verdict**: Intellectually elegant but harder to validate quantitatively. "Torsion entropy explains polymerization selectivity" is a qualitative claim that may not produce clean numbers for a top venue. Better positioned as a follow-up or supplementary contribution.

---

## Eliminated Ideas

- **Idea 6** (Reactive Bonding): Too ambitious; requires fundamental sGNN changes. Follow-up work.
- **Idea 7** (Transfer Learning): Low novelty — fragment library already published.
- **Idea 9** (Full PhyNEO-Polymer Electrolyte): Too many moving parts. Long-term goal.
- **Idea 10** (Few-Shot): Medium novelty, better as supplementary result.

---

## Refined Proposal

- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Tracker: `refine-logs/EXPERIMENT_TRACKER.md`

### Key Infrastructure Findings

From codebase analysis of PhyNEO-Electrolyte:

- **sGNN scales to 10K atoms** — benchmark code exists (`benchmark_sgnn_dme_10k/`)
- **60x GPU speedup** via sparse matrix operations (PyTorch, documented in sgnn_fast.py)
- **OpenMM TorchForce integration** works — energy match to floating-point precision verified
- **Three integration paths**: CallbackPyForce, TorchForce (JIT traced), Tiled (replicated topology)
- **Known issue**: MD stability — NaN after ~100ps in NPT reported; needs debugging
- **Variable-cell (NPT)**: Supported via TorchForce (not CallbackPyForce)

### Two-Track Strategy

| Track | Method | Speed | Accuracy | Risk |
|-------|--------|-------|----------|------|
| A (preferred) | Direct sGNN-MD in OpenMM | ~0.5-2 ns/day @5K atoms (est.) | Full DFT accuracy | MD stability, speed |
| B (fallback) | sGNN-refit OPLS torsions → classical MD | ~50-200 ns/day | DFT torsions + classical NB | Limited improvement scope |

**Decision gate**: Block 0 experiments (sGNN speed benchmark at 5K atoms)

---

## Next Steps

- [ ] Run Block 0: sGNN speed benchmark + MD stability test (IMMEDIATE)
- [ ] Start Block 1.1: PMMA DFT data generation (can run in parallel)
- [ ] After Block 0: Decide Track A vs Track B
- [ ] `/run-experiment` to deploy experiments from the plan
- [ ] `/auto-review-loop` to iterate until submission-ready
- [ ] Or invoke `/research-pipeline` for the complete end-to-end flow

---

## Sources

- [SimPoly: ML Force Fields for Polymers](https://arxiv.org/abs/2510.13696) — Simm et al., Microsoft Research, 2025
- [PhyNEO-Electrolyte: Hybrid Physics-Driven NN Force Field](https://arxiv.org/abs/2511.13294) — Chen et al., 2025
- [PhyNEO: Neural-Network-Enhanced Physics-Driven Force Field](https://pubs.acs.org/doi/10.1021/acs.jctc.3c01045) — JCTC, 2023
- [Scalable sGNN for Large Flexible Organic Molecules](https://pubs.acs.org/doi/10.1021/acs.jpclett.1c02214) — JPCL, 2021
- [Foundation MLIP with Polarizable Long-Range Interactions](https://www.nature.com/articles/s41467-025-65496-3) — Nature Comms, 2025
- [QRNN: Charges and Long-Range from Energies/Forces](https://www.nature.com/articles/s41467-025-63852-x) — Nature Comms, 2025
- [Reactive MLFF for Crosslinked Epoxy](https://link.springer.com/article/10.1007/s10118-025-3389-4) — Chinese J. Polymer Sci., 2025
- [Universal MLIPs for Mechanical Properties](https://arxiv.org/abs/2511.22885) — Stracke et al., 2025 (MOFs/inorganics only)
- [MLIP-Accelerated Redox Potentials](https://pubs.acs.org/doi/10.1021/jacs.4c01221) — JACS, 2024
- [On-the-Fly MLFF for Polymer Glass Transition](https://arxiv.org/abs/2601.17137) — 2026
- [BAMBOO: Predictive ML Framework for Electrolytes](https://www.nature.com/articles/s42256-025-01009-7) — Nature Machine Intelligence, 2025
- [Domain Universal MLIP for Battery Electrolytes](https://www.nature.com/articles/s41467-025-67982-0) — Nature Comms, 2025
- [Physics-Constrained Data Augmentation for Bond Dissociation](https://pubs.acs.org/doi/10.1021/acs.jcim.4c01847) — JCIM, 2024
- [Polymer MD System Size for Mechanical Properties](https://pubs.acs.org/doi/10.1021/acs.jpcb.4c00845) — JPCB, 2024
