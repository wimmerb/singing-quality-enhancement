# Quality Enhancement of Overdub Singing Voice Recordings
[Audio Examples](https://wimmerb.github.io/singing-quality-enhancement/)

[Thesis](https://github.com/wimmerb/singing-quality-enhancement/blob/master/quality-enhancement-of-overdub-singing-recordings.pdf)

This page is currently under construction.

# Abstract
Singing enhancement aims to improve the perceived quality of a singing recording in various aspects. 
Focusing on the aspect of removing degradation such as background noise or room reverberation, singing enhancement is related to the topic of speech enhancement. 
In this work, two neural network architectures for speech denoising – namely FullSubNet and Wave-U-Net – were trained and evaluated specifically on denoising of user singing voice recordings. 
While both models show similar performance as for speech denoising, FullSubNet outperforms Wave- U-Net on this task. Furthermore, the removal of sound leakage (i.e. reference signal/accompaniment for overdubbing that becomes audible in the background of a recording) was performed with a novel modification of FullSubNet. 
The proposed architecture performs leakage removal by taking the signal leading to aforementioned leakage as an additional input. For the case of choir music and for leakage removal, this modified FullSubNet architecture was compared to the original FullSubNet architecture. 
Evaluation results show its overall efficacy on leakage removal as well as significant benefits introduced by usage of the additional input.

# Results
## Audio examples
To get a first impression, please have a listen to these [examples](https://wimmerb.github.io/singing-quality-enhancement/)
## Pretrained Models
You can find pretrained models in the **[Experiments](https://github.com/wimmerb/singing-quality-enhancement/tree/master/Experiments)** folder. For each model, a readme file in its parent folder will give instructions on how to use it.

# Prerequisites

## Submodule initialization
Please use the following instructions:
```bash
# Initialize all submodules
git submodule update --init --recursive

# Change branch to stay up-to-date
cd SpeechEnhancers && git checkout main
cd audio_zen && git checkout main
```

```bash
# Do not forget to pull from time to time
git pull --recurse-submodules

# OR (pulls only submodules)
git submodule update --remote
```

## Environment

Please use the following instructions (conda installation required):

```bash
# Install conda environment and python packages
conda env create -f environment.yaml

# Activate conda environment
conda activate SING_QUAL_EN
```

# Dataset Handling
**Please have a look at the [Datasets](https://github.com/wimmerb/singing-quality-enhancement/tree/master/Datasets) folder for preprocessing code and further information. A list of usefuul datasets is linked aswell.**

Note that, generally, raw audio file sources are handled via text files. These files contain lists with individual file paths. They are given to the training script and dynamically applied or used for precomputing datasets for validation and testing.
## Preprocessing Scripts
To prepare the training data, a processing pipeline with multiple steps is applied. In this pipeline, desired subsets of datasets are selected, segmented/balanced and combined to audio file path lists. For example, a result of the pipeline could be three text files for noise profiles (*training/validation/testing*) and three text files for voice recordings (same split). 

These file lists are then dynamically combined during training (the *training* split) or for precomputing static datasets for comparable validation and testing (the *validation/testing* splits).




# Training
For detailed information on the training process, please refer to the "Methods for ..." chapters in [this thesis document](https://github.com/wimmerb/singing-quality-enhancement/blob/master/quality-enhancement-of-overdub-singing-recordings.pdf). Before starting the training process, please make sure that you have the specified file path lists and properly precomputed validation (and optionally testing) datasets at hand.
## Denoising
### Training
```bash
# Go to directory for architecture-specific processing (inside recipes folder)
cd SpeechEnhancers/recipes/thesis_experiments_fsn 

# Start training
python train.py -C denoise_fsn/train.toml -N 1
# OR resume training
python train.py -C denoise_fsn/train.toml -R -N 1
```

### Evaluation
```bash
# Go to directory for architecture-specific processing (inside recipes folder)
cd SpeechEnhancers/recipes/thesis_experiments_fsn

# Evaluate the best model (Same as resuming and running validation only)
python train.py -C denoise_fsn/train.toml -R -V -N 1
```


## Leakage Removal
### Training

Example:

```bash
# Go to directory for architecture-specific processing (inside recipes folder)
cd SpeechEnhancers/recipes/thesis_experiments_fsn 

# Start training
python train.py -C leakage_removal/fullsubnet_aec/train_BGM_full_dual.toml -N 1
# OR resume training
python train.py -C leakage_removal/fullsubnet_aec/train_BGM_full_dual.toml -R -N 1
```
### Evaluation

Example:

```bash
# Go to directory for architecture-specific processing (inside recipes folder)
cd SpeechEnhancers/recipes/thesis_experiments_fsn

# Evaluate the best model (Same as resuming and running validation only)
python train.py -C leakage_removal/fullsubnet_aec/train_BGM_full_dual.toml -R -V -N 1
```

# Inference
You can find pretrained models in the **[Experiments](https://github.com/wimmerb/singing-quality-enhancement/tree/master/Experiments)** folder. For each model, a readme file in its parent folder will give instructions on how to use it.

Example usage:

```
# Go to directory for architecture-specific processing (inside recipes folder)
cd SpeechEnhancers/recipes/thesis_experiments_fsn 

# Enhance with given model and output paths
python inference.py -C denoise_fsn/inference.toml -M ../../../Experiments/Denoising/FullSubNet/denoise_FSN/checkpoints/best_model.tar -O ../../../Experiments/Denoising/FullSubNet/denoise_FSN/inference
