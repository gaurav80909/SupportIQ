import os
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Download Twitter Customer Support dataset from Kaggle")
    parser.add_argument("--output", type=str, default="data/raw", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = out_dir / "twcs.csv"
    if csv_path.exists():
        logger.info(f"Data already exists at {csv_path}")
        return

    logger.info("Downloading dataset from Kaggle using kaggle CLI...")
    # NOTE: Requires kaggle CLI to be installed and credentials configured in ~/.kaggle/kaggle.json
    os.system(f"kaggle datasets download -d thoughtvector/customer-support-on-twitter -p {out_dir} --unzip")
    
    if csv_path.exists():
        logger.info("Download and extraction successful.")
    else:
        logger.error("Download failed or twcs.csv not found.")

if __name__ == "__main__":
    main()
