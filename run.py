
import argparse
import os, errno
import sys
sys.path.append('../')

import Generator.layout_process.gen_layout as gl
from Generator.data_process.data_loader import DataLoader
import Generator.layout_process.gen_box as gb
import pickle

def parse_arguments():
    
    parser = argparse.ArgumentParser(
        description="Generate synthetic pdf data for text recognition."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="Directory where the final output will be stored",
        default="/root/storage/Experiments/vision/Generator/asset/out"
    )
    parser.add_argument(
        "-t",
        "--text_folder",
        type=str,
        help="Directory where text image stored",
        default="/root/storage/Experiments/vision/Generator/asset/text/out"
    )
    parser.add_argument(
        "-b",
        "--back_ground_file",
        type=str,
        help="Define background image behind generated layouts",
        default="/root/storage/Experiments/vision/Generator/asset/bg/plain_white.png"
    )
    parser.add_argument(
        "-i",
        "--iteration",
        type=int,
        help="Define how many output file generated",
        default=1
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
    
    #TODO) check the file format
    if not os.path.exists(args.back_ground_file):
        raise FileNotFoundError('background file must be specified')
    
    dataloader = DataLoader(args.text_folder,args.back_ground_file)
    
    #trial = num of gen
    
    json = []
    for i in range(args.iteration):
        rects = gl.gen_layout()
        sentences, palette = gb.gen_box(dataloader, rects)
        palette.save(os.path.join(args.output_dir,str(i)+'.png'))
        temp = { '{}.png'.format(i):sentences }
        json.append(temp)
    with open(os.path.join(args.output_dir,'trial.pkl'),'wb') as f:
        pickle.dump(json,f)
    

if __name__ == "__main__":
    main()