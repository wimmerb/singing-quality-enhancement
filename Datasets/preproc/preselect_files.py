import os
import glob
from pathlib import Path

# ============MODIFY HERE============
# produces 68 mono files with Aachen Impulse Response Database (https://www.iks.rwth-aachen.de/en/research/tools-downloads/databases/aachen-impulse-response-database/)
out_fn = "GATHERED_DATA/rir_AIR.txt"
path = "AIR_1_4"
and_conditions = {
    "hfrp": False
}
or_conditions = {
    "meeting": True,
    "bathroom": True,
    "kitchen": True,
    "office": True,
    "booth": True
}
# ============MODIFY END=============

out_fn = "/home/benedikt/thesis/TRAIN_EVALUATION_DATA/DENOISING_21_06_24/TEST_SET_CANTAMUS_REAL/info/TEST_SET_CANTAMUS_REAL.txt"
path = "/home/benedikt/thesis/TRAIN_EVALUATION_DATA/DENOISING_21_06_24/TEST_SET_CANTAMUS_REAL"
and_conditions = {
}
or_conditions = {
}


print ("gathering...")
nfiles = 0
with open(out_fn, 'w') as handle: 
    for filename in Path(path).rglob('*.wav'):
        #checking conditions that *ALL* need to be fulfilled
        if and_conditions:
            and_valid = True
            for word, expected in and_conditions.items():
                if (word in str(filename).lower()) != expected:
                    print ("NOT valid", filename)
                    and_valid = False
                    break
            if not and_valid: continue

        #checking conditions of which *AT LEAST ONE* needs to be fulfilled
        if or_conditions:
            or_valid = False
            for word, expected in or_conditions.items():
                if (word in str(filename).lower()) == expected:
                    or_valid = True
                    break
            if not or_valid: continue
        
        handle.write(str(filename.absolute())+"\n")
        nfiles += 1

print (f"finished: {nfiles} files satisfy path and condition, stored to {out_fn}")


# ============CLEAN=============CLEAN==============CLEAN=============CLEAN==============

# produces 10325 files
# out_fn = "GATHERED_DATA/clean_VSED.txt"
# path = "VSED"
# and_conditions = {
#    "clean": True,
# }
# or_conditions = {}

# produces 88328 files
# out_fn = "GATHERED_DATA/clean_VCTK.txt"
# path = "VCTK"
# and_conditions = {}
# or_conditions = {}

# produces 139 files
# out_fn = "GATHERED_DATA/clean_VOCAL_SET.txt"
# path = "VOCAL_SET"
# and_conditions = {}
# or_conditions = {
#     "excerpts": True,
# }

# ============CLEAN=============CLEAN==============CLEAN=============CLEAN==============


# ============NOISE=============NOISE==============NOISE=============NOISE==============

# produces 80 mono files
# out_fn = "GATHERED_DATA/noise_DEMAND.txt"
# path = "DEMAND"
# or_conditions = {
#     "kitchen": True,
#     "washing": True,
#     "river": True,
#     "hallway": True,
#     "office": True,
# }
# and_conditions = {}

# produces 710 mono files
# out_fn = "GATHERED_DATA/noise_ACE.txt"
# path = "ACE"
# and_conditions = {"noise_fan": True}
# or_conditions = {}

# produces 480 mono files
# out_fn = "GATHERED_DATA/noise_REVERB_TOOLS.txt"
# path = "REVERB_TOOLS"
# and_conditions = {"noise": True}
# or_conditions = {}

# produces 99 mono files
# out_fn = "GATHERED_DATA/noise_LAPTOP_NOISE.txt"
# path = "LAPTOP_NOISE"
# and_conditions = {}
# or_conditions = {}

# ============NOISE=============NOISE==============NOISE=============NOISE==============




# ============RIR=============RIR==============RIR=============RIR==============
# produces 408 mono files
# out_fn = "GATHERED_DATA/rir_ACE.txt"
# path = "ACE"
# and_conditions = {
#     "rir": True,
#     "403": False,
#     "508": False,
#     "lobby": False
# }
# or_conditions = {}

# produces 64 mono files
# out_fn = "GATHERED_DATA/rir_REVERB_TOOLS"
# path = "REVERB_TOOLS"
# and_conditions = {
#     "rir": True,
#     "smallroom": True,
# }
# or_conditions = {}

# produces 20000 mono files
# out_fn = "GATHERED_DATA/rir_simulated_rirs_16k.txt"
# path = "SIMULATED_RIRS_16K"
# and_conditions = {
#     "smallroom": True
# }
# or_conditions = {}

# produces 68 mono files
# out_fn = "GATHERED_DATA/rir_AIR.txt"
# path = "AIR_1_4"
# and_conditions = {
#     "hfrp": False
# }
# or_conditions = {
#     "meeting": True,
#     "bathroom": True,
#     "kitchen": True,
#     "office": True,
#     "booth": True
# }

# ============RIR=============RIR==============RIR=============RIR==============


# ============MIR=============MIR==============MIR=============MIR==============
# produces 130 files
# out_fn = "GATHERED_DATA/mir_VINTAGE_MICS.txt"
# path = "VINTAGE_MICS"
# and_conditions = {
# }
# or_conditions = {
# }
# ============MIR=============MIR==============MIR=============MIR==============