import os
import sys
from sklearn.utils import resample, shuffle
import numpy as np
from pathlib import Path
from collections import defaultdict

# was used for data denoise/dereverb
# settings = {
#     "clean_VCTK.txt": {
#         "resample": 20000,
#         "sort_func": (lambda x: Path(x).parts[-2]),
#         "destinations": {
#             "clean_TRAIN.txt": 0.8,
#             "clean_VALIDATION.txt": 0.2,
#         },
#     },
#     "clean_VSED.txt": {
#         "resample": 20000,
#         "sort_func": (lambda x: Path(x).parts[-2]),
#         "destinations": {
#             "clean_TRAIN.txt": 0.8,
#             "clean_VALIDATION.txt": 0.2,
#         },
#     },
#     "clean_VOCAL_SET.txt": {
#         "resample": None,
#         "sort_func": (lambda x: Path(x).parts[-4]),
#         "destinations": {
#             "clean_TEST.txt": 1.0,
#         },
#     },
#     "noise_DEMAND.txt": {
#         "resample": 400,
#         "sort_func": (lambda x: Path(x).parts[-2]),
#         "destinations": {
#             "noise_TRAIN.txt": 0.7,
#             "noise_VALIDATION.txt": 0.15,
#             "noise_TEST.txt": 0.15,
#         },
#     },
#     "noise_LAPTOP_NOISE.txt": {
#         "resample": 800, # represent this more because it has keyboard clicks (non-static noise)
#         "sort_func": (lambda x: Path(x).parts[-1].split('_')[0]),
#         "destinations": {
#             "noise_TRAIN.txt": 0.7,
#             "noise_VALIDATION.txt": 0.15,
#             "noise_TEST.txt": 0.15,
#         },
#     },
#     "noise_ACE.txt": {
#         "resample": 400,
#         "sort_func": (lambda x: Path(x).parts[-3]),
#         "destinations": {
#             "noise_TRAIN.txt": 0.7,
#             "noise_VALIDATION.txt": 0.15,
#             "noise_TEST.txt": 0.15,
#         },
#     },
#     "noise_REVERB_TOOLS.txt": {
#         "resample": 350, # 350 because 400*0.7 = 280 = 350*0.8 to balance train set
#         "sort_func": (lambda x: Path(x).parts[-1].split('_')[1]),
#         "destinations": {
#             "noise_TRAIN.txt": 0.8,
#             "noise_VALIDATION.txt": 0.2,
#         },
#     },
#     "rir_simulated_rirs_16k.txt": {
#         "resample": 570, #target: 400 files in training
#         "sort_func": (lambda x: Path(x).parts[-2]),
#         "destinations": {
#             "rir_TRAIN.txt": 0.7,
#             "rir_VALIDATION.txt": 0.15,
#             "rir_TEST.txt": 0.15,
#         },
#     },
#     "rir_ACE.txt": {
#         "resample": 500, #target: 400 files in training
#         "sort_func": (lambda x: Path(x).parts[-3]),
#         "destinations": {
#             "rir_TRAIN.txt": 0.8,
#             "rir_VALIDATION.txt": 0.2,
#         },
#     },
#     "rir_REVERB_TOOLS.txt": {
#         "resample": 400,
#         "sort_func": (lambda x: Path(x).parts[-1].split('_')[1]),
#         "destinations": {
#             "rir_TRAIN.txt": 1.0,
#         },
#     },
#     "rir_AIR.txt": {
#         "resample": 400,
#         "sort_func": (lambda x: Path(x).parts[-1]),
#         "destinations": {
#             "rir_TRAIN.txt": 1.0,
#         },
#     },
#     "mir_VINTAGE_MICS.txt": {
#         "resample": 68,
#         "sort_func": (lambda x: Path(x).parts[-1]),
#         "destinations": {
#             "mir_TRAIN.txt": 0.7,
#             "mir_VALIDATION.txt": 0.15,
#             "mir_TEST.txt": 0.15,
#         },
#     },
# }
#    #target_dir = "/home/benedikt/thesis/datasets/TRAIN_VALIDATE_TEST/2021_06_23"
# target_dir = "/home/benedikt/thesis/TRAIN_EVALUATION_DATA/DENOISING_21_06_24/data_source_paths"

settings = {
    "rir_simulated_rirs_16k.txt": {
        "resample": 570, #target: 400 files in training
        "sort_func": (lambda x: Path(x).parts[-2]),
        "destinations": {
            "rir_TRAIN.txt": 0.7,
            "rir_VALIDATION.txt": 0.15,
            "rir_TEST.txt": 0.15,
        },
    },
    "rir_ACE.txt": {
        "resample": 500, #target: 400 files in training
        "sort_func": (lambda x: Path(x).parts[-3]),
        "destinations": {
            "rir_TRAIN.txt": 0.8,
            "rir_VALIDATION.txt": 0.2,
        },
    },
    "rir_REVERB_TOOLS.txt": {
        "resample": 400,
        "sort_func": (lambda x: Path(x).parts[-1].split('_')[1]),
        "destinations": {
            "rir_TRAIN.txt": 1.0,
        },
    },
    "rir_AIR.txt": {
        "resample": 400,
        "sort_func": (lambda x: Path(x).parts[-1]),
        "destinations": {
            "rir_TRAIN.txt": 1.0,
        },
    },
    "mir_VINTAGE_MICS.txt": {
        "resample": 400,
        "sort_func": (lambda x: Path(x).parts[-1]),
        "destinations": {
            "mir_TRAIN.txt": 0.7,
            "mir_VALIDATION.txt": 0.15,
            "mir_TEST.txt": 0.15,
        },
    },
}

target_dir = "/home/benedikt/thesis/TRAIN_EVALUATION_DATA/LEAKAGE_REMOVAL/data_splitting_1"


# create target directory if it is non-existent
if not os.path.exists(Path(target_dir)):
    os.makedirs (Path(target_dir))



destinations_dct = defaultdict(list)
#for debugging identity split
identity_split_dct = defaultdict(list)

for source_fn, processing in settings.items():
    with open (source_fn, 'r') as source_file:
        entry_list = np.array ([line.strip('\n') for line in source_file.readlines()])
        entry_list = sorted (resample (entry_list, n_samples = processing['resample']))

        #code to instantiate ordering by given "identity"
        identity_list = shuffle (list({processing["sort_func"] (x) for x in entry_list}))
        entries_reordered = sorted (entry_list, key = (lambda x: identity_list.index (processing["sort_func"] (x))))

        split_start = 0
        split_end = 0
        for destination_fn, proportion in processing["destinations"].items():
            split_start = split_end
            split_end = int (np.floor (proportion * len (entries_reordered))) + split_start

            identity_split_dct[destination_fn] += [processing["sort_func"] (x) for x in entries_reordered[split_start:split_end]]
            destinations_dct[destination_fn] += entries_reordered[split_start:split_end]


for destination_fn, entries in destinations_dct.items ():
    destinations_dct[destination_fn] = shuffle (entries)

for destination_fn, entries in destinations_dct.items ():
    with open (os.path.join (target_dir, destination_fn), 'w') as dest_file:
        dest_file.writelines (line + '\n' for line in entries)

for destination_fn, identities in identity_split_dct.items ():
    print (destination_fn, ":", set(identities))
