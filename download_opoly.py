import os
import argparse
from huggingface_hub import snapshot_download

def download_dataset(token, local_dir="./data"):
    print(f"Downloading OPoly26 dataset to {local_dir}...")
    try:
        # Note: OPoly26 is part of the OMol25 repository on Hugging Face.
        # It's a gated repository, so a token is required.
        snapshot_download(
            repo_id="facebook/OMol25",
            local_dir=local_dir,
            token=token,
            repo_type="dataset",
            # If you want specific files only, you can use allow_patterns
            # allow_patterns=["poly26*"] 
        )
        print("Download complete.")
    except Exception as e:
        print(f"Error during download: {e}")
        print("Please ensure you have requested access at https://huggingface.co/facebook/OMol25")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download OPoly26 dataset from Hugging Face.")
    parser.add_argument("--token", type=str, required=True, help="Your Hugging Face Access Token")
    parser.add_argument("--dir", type=str, default="./data", help="Directory to save the dataset")
    
    args = parser.parse_args()
    download_dataset(args.token, args.dir)
