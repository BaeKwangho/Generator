
import argparse
import os, errno
import sys
from Data_loader import DataLoader

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate synthetic pdf data for text recognition."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="Directory where the final output will be stored",
        default="out/"
    )
    parser.add_argument(
        "-t",
        "--text_folder",
        type=str,
        help="Directory where text image stored",
        default="txt/"
    )
    parser.add_argument(
        "-b",
        "--back_ground_folder",
        type=str,
        help="Directory where back-ground image stored",
        default="bg/"
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  
    
    if not os.path.isdir(args.text_folder):
        raise OSError('text folder is not exist')
    
    loader = DataLoader(args.text_folder,args.back_ground_folder)

if __name__ == "__main__":
    main()