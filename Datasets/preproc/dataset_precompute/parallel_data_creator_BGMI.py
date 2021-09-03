# THIS SCRIPT IS USED FOR CREATION OF PARALLEL BGMI DATA (AUGMENTED/MIXTURE VS BACKGROUND VS CLEAN) DATA FOR VALIDATION/TESTING/(TRAINING)
# Called like such: "python parallel_data_creator_BGMI.py -C creator_setting_BGMI.toml"

import argparse
import os
import random
import sys

import numpy as np
import toml
import torch

import torch.multiprocessing as mp

sys.path.append("/home/benedikt/thesis/repos/FullSubNet")
from audio_zen.utils import initialize_module
from audio_zen.acoustics.feature import save_wav
import tqdm

import shutil

# TODO add option to run without early stoppage and also to perform unaligned data. Might be interesting for testing especially (only 12 files is not so much...).

def create_dataset(config, noisy_dir, clean_dir, bgm_dir, info_dir):
    #print (rank)
    #print (world_size)
    
    
    # initialize dataset
    dataset=initialize_module(
        config["dataset"]["path"],
        args=config["dataset"]["args"])

    # set limit to created files
    file_limit = config["meta"]["file_limit"]

    # number of iterations says how often we want to cycle through all pieces (when there are not so many pieces)
    nr_data_cycles = config["meta"].get("nr_data_cycles", 1)
    assert nr_data_cycles > 0, "cannot do negative number of data cycles"

    using_aligned = config['dataset']['args']['aligned_prob'] == 1.0

    file_names = []
    for i in tqdm.tqdm(range(file_limit)):
        
        if using_aligned and ((dataset.grouped_by_piece == {}) and (dataset.mix_buffer == [])):
            nr_data_cycles -= 1
            if nr_data_cycles <= 0:
                print ("early stoppage (out of file sources and cycles)")
                break
            else:
                dataset=initialize_module(
                    config["dataset"]["path"],
                    args=config["dataset"]["args"])

        clean, noisy, _, bgm, piece_id, snr = dataset[i]
        fn = f"{str(i).zfill(5)}__{piece_id}.wav"
        #fn = dataset.pop_current_filename()
        #fn = piece_id
        file_names.append(fn)
        save_wav(os.path.join(
            noisy_dir, fn), 
            noisy, 
            config["dataset"]["args"]["sr"]
            )
        save_wav(os.path.join(
            bgm_dir, fn), 
            bgm, 
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

    print (configuration['meta']['save_dir'],  ": PARALLEL DATA (MIXTURE(NOISY), BGM, CLEAN) CREATED")


    

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
    bgm_dir = os.path.join(target_dir, "bgm")
    clean_dir = os.path.join(target_dir, "clean")
    
    info_dir = os.path.join(target_dir, "info")

    print (configuration["dataset"]["args"]["mir_list_fn"])
    if not os.path.exists(target_dir):
        os.makedirs (noisy_dir)
        os.makedirs (bgm_dir)
        os.makedirs (clean_dir)
        os.makedirs (info_dir)

        shutil.copy(args.configuration, info_dir)
        shutil.copy(configuration["dataset"]["args"]["file_list_fn"], info_dir)
        shutil.copy(configuration["dataset"]["args"]["rir_list_fn"], info_dir)
        shutil.copy(configuration["dataset"]["args"]["mir_list_fn"], info_dir)

        create_dataset(config=configuration, noisy_dir=noisy_dir, clean_dir=clean_dir, bgm_dir=bgm_dir, info_dir=info_dir)
    else:
        print (f"target_dir (configuration['meta']['save_dir']) {configuration['meta']['save_dir']} already exists")
    
    