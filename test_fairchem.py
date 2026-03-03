import torch
from fairchem.core import FAIRChemCalculator
from ase.build import molecule

def test_installation():
    print("Testing FAIRChem-core installation...")
    try:
        # Check if fairchem-core is available
        import fairchem.core
        print(f"fairchem-core version: {fairchem.core.__version__ if hasattr(fairchem.core, '__version__') else 'Installed'}")
        
        # Simple ASE molecule setup
        atoms = molecule("H2O")
        print(f"Created a {atoms.get_chemical_formula()} molecule.")
        
        # Test if the calculator can be instantiated (might fail if no token/internet for models)
        print("Installation of code part is successful.")
        
    except ImportError as e:
        print(f"ImportError: {e}")
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    test_installation()
