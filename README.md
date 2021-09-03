# Quality Enhancement of Overdub Singing Voice Recordings
[DEMO](https://wimmerb.github.io/singing-quality-enhancement/)

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
You can find pretrained models in the **Experiments** folder. For each model, a readme file in its parent folder will give instructions on how to use it.

# Dependencies
Please use the following instructions (conda installation required):

```bash
# Install conda environment and python packages
conda env create -f environment.yaml

# Activate conda environment
conda activate SING_QUAL_EN
```
# Denoising
## Data Augmentation
## Models
# Leakage Removal
## Data Augmentation
## Models

# Dataset Handling
## Preprocessing Scripts
## Laptop noises from Freesound
