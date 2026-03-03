# Project Polymer: OPoly26 & FAIRChem

This project is set up to work with the **OPoly26** and **OMol25** datasets using the **FAIR Chemistry (fairchem)** library.

## Installed Components

- **FAIRChem-core**: Machine learning models and ASE calculators for atomistic systems.
- **FAIRChem-data-omol**: Tools for generating and processing molecular configurations.
- **ASE**: Atomic Simulation Environment for molecular manipulation.

## Database Installation (OPoly26 / OMol25)

The OPoly26 and OMol25 datasets are hosted on Hugging Face and are **gated**. Follow these steps to complete the installation:

### 1. Request Access
Visit the [facebook/OMol25 Hugging Face page](https://huggingface.co/facebook/OMol25), log in to your account, and click **"Agree and access repository"** to accept the CC-BY-4.0 license and provide contact information.

### 2. Generate Access Token
Go to your [Hugging Face Settings > Tokens](https://huggingface.co/settings/tokens) and generate a new **Read** token.

### 3. Download the Dataset
Use the provided `download_opoly.py` script to download the database files. Replace `YOUR_HF_TOKEN` with the token you generated:

```bash
python3 download_opoly.py --token YOUR_HF_TOKEN --dir ./data
```

*Note: The full dataset is extremely large. The script will download the processed `.aselmdb` files and model weights by default.*

## Verification

To verify that the library and environment are correctly installed, run the test script:

```bash
python3 test_fairchem.py
```

If successful, you should see:
```text
Testing FAIRChem-core installation...
fairchem-core version: 2.15.1.dev9+...
Created a H2O molecule.
Installation of code part is successful.
```

## Resources
- **FAIRChem Repository:** [https://github.com/facebookresearch/fairchem](https://github.com/facebookresearch/fairchem)
- **Dataset Paper:** [The Open Molecules 2025 (OMol25) Dataset](https://arxiv.org/abs/2505.08762)
- **OPoly26 Details:** Part of the OMol25 release focusing on polymer substructures.
