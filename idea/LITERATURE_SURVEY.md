# Literature Survey: ML Potentials for Polymer/Electrolyte with Bonding Interactions

**Date**: 2026-03-24
**Direction**: General bonding interaction machine-learning potential for polymer or electrolyte

---

## 1. Research Landscape Overview

### 1.1 Current State of MLIPs for Polymers & Electrolytes

The field sits at a critical inflection point: **universal foundation MLIPs** (MACE-MP-0, CHGNet, M3GNet, PFP) can handle broad chemical space but lack polymer-specific physics (bonding topology, long chains, mechanical response). Meanwhile, **polymer-specific classical FFs** (OPLS-AA, GAFF2, COMPASS) scale well but have poor accuracy for reactive chemistry and new chemistries.

**Key players:**
- **SimPoly / Vivace** (Microsoft, Oct 2025): First MLFF to predict polymer densities and Tg ab initio for 130 diverse polymers. Outperforms classical FFs on density. Introduced PolyArena benchmark. *Limitation*: No explicit bonding/non-bonding decomposition; no reactive chemistry; no mechanical properties reported.
- **PhyNEO-Electrolyte** (Chen, Gao, Yu et al., Nov 2025): Hybrid physics+NN for liquid electrolytes. Decomposes energy into bonding (sGNN) and non-bonding (multipole + Slater + NN correction). Uses EDA data for extreme data efficiency. *Limitation*: Developed for small-molecule electrolytes, not polymers. No mechanical property predictions.
- **BAMBOO** (ByteDance): Predictive MLFF framework for liquid electrolyte MD. Good for battery electrolyte properties.
- **Domain-oriented universal MLIP for battery electrolytes** (Nature Comms 2025): Iterative training on diverse electrolyte compositions.

### 1.2 Bonding vs Non-Bonding Decomposition

PhyNEO's approach is unique in the field:
- **Non-bonding**: Asymptotic (multipole, polarizability, dispersion) + Slater short-range (from EDA) + pairwise NN correction
- **Bonding**: Sub-graph neural network (sGNN) operating on bond-centric subgraphs
- This decomposition enables: (a) correct long-range behavior, (b) data efficiency, (c) transferability across chemical space

**sGNN Architecture** (from codebase analysis):
- Bond-centric subgraphs (not atom-centric like NequIP/MACE)
- 188 input features: 160 atom-type one-hot + 28 geometric (bonds, angles, dihedrals)
- Linear gating message passing (fast, not full MLP)
- Permutation averaging for symmetry
- Energy = sum of per-bond contributions
- Currently handles: DMC, EC, PF6, BF4, DFP monomers

### 1.3 Reactive MLIPs

- **Reactive MLFF for crosslinked epoxy** (Chinese J. Polymer Sci., 2025): Captures bond breaking/formation in thermoset curing. RMSE: 1.3 meV/atom, 159 meV/Å. 1200x faster than AIMD.
- **Physics-constrained data augmentation** (JCIM, 2024): Uses Morse potential constraints to fix bond dissociation curves in MLIPs. Near coupled-cluster accuracy.
- **PFP/MM hybrid** (2026): Universal NN potential + classical FF for large-scale reactive simulations.

### 1.4 Long-Range Interactions

- **Foundation MLIP with polarizable long-range** (Nature Comms, 2025): Equivariant GNN + polarizable charge equilibration. Directly optimizes electrostatic energies (not charges).
- **QRNN** (Nature Comms, 2025): Learns charges and long-range interactions from energies/forces. Global charge equilibration.
- **Latent Ewald Summation (LES)**: Captures long-range electrostatics without explicit charges.
- **PiNet2** (JCTC, 2025): Equivariant architecture for electrochemical systems with charge/dipole prediction.

### 1.5 Mechanical Properties of Polymers

- **Still dominated by classical FFs**: OPLS-AA for polyimides (Young's modulus, Poisson's ratio). GAFF2 for general polymers.
- **ML approaches are property-prediction only**: polyGNN predicts Young's modulus (RMSE 0.827 GPa) from molecular structure, but does NOT use MD simulation — just structure→property mapping.
- **No MLIP-driven mechanical property simulation exists** for polymers. This is a major gap.
- **On-the-fly MLFF for polymer glass transition** (arXiv 2601.17137, Jan 2026): Active learning MLFF for Tg prediction via MD.

### 1.6 Application-Specific Gaps

**Redox potential for Li-S separators:**
- ML models predict redox potentials for organic molecules (graph-based GPR, hybrid kernels)
- No MLIP-based approach to screen polymer membranes by electrochemical stability
- Classical DFT calculations used for monomer-level screening

**Reaction pathways & torsion entropy:**
- Torsional barriers poorly captured by OPLS (exaggerated barriers)
- QRNN-based ML corrections to torsional potentials show improvement
- Conformational entropy from dihedral sampling is qualitatively predictive of polymerization

**CO2 capture mechanical properties:**
- Active area: PIMs, polybenzimidazole membranes for CO2 separation
- MD used for gas permeability, diffusivity
- Mechanical property changes with CO2 absorption: NO ML-based study exists
- Experimentalists need: how does modulus change with carbonate incorporation? Can we identify polymers unsuitable for scalable processes?

---

## 2. Structural Gaps Identified

### Gap A: No general bonding MLIP for polymers
SimPoly doesn't decompose bonding/non-bonding. PhyNEO does but only for small-molecule electrolytes. No one has extended the PhyNEO bonding/non-bonding framework to polymers.

### Gap B: No MLIP-driven mechanical property prediction
All polymer mechanical property predictions use either classical FFs or structure→property ML (no simulation). An accurate MLIP could predict stress-strain curves, moduli, and failure from first principles.

### Gap C: No reactive MLIP for polymer electrolyte interfaces
Reactive chemistry at electrode-electrolyte interfaces, SEI formation, polymer degradation — all require reactive potentials that also handle long-range electrostatics. Current reactive MLIPs are for specific systems only.

### Gap D: No MLIP for polymer-gas interaction mechanical response
CO2/gas absorption in polymers changes mechanical properties. Classical FFs cannot capture the electronic effects of carbonate incorporation. MLIP could bridge this gap.

### Gap E: Redox stability screening with MLIP accuracy
Current screening uses monomer-level DFT. A transferable MLIP could enable polymer-level redox stability assessment with conformational sampling.

---

## 3. Key References

1. SimPoly (Simm et al., 2025) - arXiv:2510.13696
2. PhyNEO-Electrolyte (Chen et al., 2025) - arXiv:2511.13294
3. Reactive MLFF for crosslinked epoxy (2025) - Chinese J. Polymer Sci.
4. Foundation MLIP with polarizable long-range (2025) - Nature Comms
5. QRNN charges and long-range (2025) - Nature Comms
6. On-the-fly MLFF for polymer Tg (2026) - arXiv:2601.17137
7. BAMBOO for liquid electrolytes (2025) - Nature Machine Intelligence
8. Domain universal MLIP for battery electrolytes (2025) - Nature Comms
9. Physics-constrained data augmentation for bond dissociation (2024) - JCIM
10. PiNet2 for electrochemical systems (2025) - JCTC
