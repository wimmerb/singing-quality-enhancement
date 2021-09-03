# THIS SCRIPT IS USED FOR CREATION OF PARALLEL (AUGMENTED, NOISY VS CLEAN) DATA FOR VALIDATION/TESTING/(TRAINING)
# Called like such: "python parallel_data_creator.py -C creator_setting.toml"

import argparse
import os
import random
import sys

import numpy as np
import toml
import torch

import torch.multiprocessing as mp

from audio_zen.utils import initialize_module
from audio_zen.acoustics.feature import save_wav
import tqdm

import shutil




def create_dataset(config, noisy_dir, clean_dir, info_dir):
    #print (rank)
    #print (world_size)
    
    
    # initialize dataset
    dynamic_dataset=initialize_module(
        config["dataset"]["path"],
        args=config["dataset"]["args"])

    # set limit to created files
    file_limit = config["meta"]["file_limit"]

    file_names = []
    for i in tqdm.tqdm(range(file_limit)):
        noisy, clean = dynamic_dataset[i]
        #fn = f"{str(i).zfill(4)}.wav"
        fn = dynamic_dataset.pop_current_filename()
        file_names.append(fn)
        save_wav(os.path.join(
            noisy_dir, fn), 
            noisy, 
            config["dataset"]["args"]["sr"]
            )
        save_wav(os.path.join(
            clean_dir, fn), 
            clean, 
            config["dataset"]["args"]["sr"]
            )
        #print (len(file_names), "of which ", len(set(file_names)), "are unique")
        #print (noisy.shape, clean.shape)
    with open (os.path.join(info_dir, "files_used.txt"), "w") as handle:
        handle.writelines([line + "\n" for line in sorted(file_names)])
    print (configuration['meta']['save_dir'],  ": PARALLEL DATA CREATED")


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FullSubNet")
    parser.add_argument("-C", "--configuration", required=True, type=str, help="Configuration (*.toml).")
    args = parser.parse_args()
    configuration = toml.load(args.configuration)

    configuration["meta"]["experiment_name"], _ = os.path.splitext(os.path.basename(args.configuration))
    configuration["meta"]["config_path"] = args.configuration

    # Create directories needed
    target_dir = configuration['meta']['save_dir']
    noisy_dir = os.path.join(target_dir, "noisy")
    clean_dir = os.path.join(target_dir, "clean")
    info_dir = os.path.join(target_dir, "info")
    if not os.path.exists(target_dir):
        os.makedirs (noisy_dir)
        os.makedirs (clean_dir)
        os.makedirs (info_dir)

        shutil.copy(args.configuration, info_dir)
        shutil.copy(configuration["dataset"]["args"]["clean_dataset"], info_dir)
        shutil.copy(configuration["dataset"]["args"]["noise_dataset"], info_dir)
        shutil.copy(configuration["dataset"]["args"]["rir_dataset"], info_dir)

        create_dataset(config=configuration, noisy_dir=noisy_dir, clean_dir=clean_dir, info_dir=info_dir)
    else:
        print (f"target_dir (configuration['meta']['save_dir']) {configuration['meta']['save_dir']} already exists")
    
    