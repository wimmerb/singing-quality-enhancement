from pathlib import Path
import librosa
import pandas as pd
import numpy as np
import os
import sys
from sklearn.utils import  shuffle

# important for split!
train_valid_split = 0.8

path_to_cantamus = "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED"

all_stems = [x.replace('\n', '_##WEIRDCHAR##_') for x in  librosa.util.find_files(path_to_cantamus)]

#blacklisting files that have only silent parts!
blacklist = [
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Messies Participatiu/Gloria - 09. Qui sedes ad dexteram Patris/voices/Bass.mp3",
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Messies Participatiu/Gloria - 09. Qui sedes ad dexteram Patris/voices/Soprano.mp3",
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Messies Participatiu/Gloria - 09. Qui sedes ad dexteram Patris/voices/Tenor.mp3",
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Messies Participatiu/Gloria - 05. Domine Deus Rex celestis/voices/Alto.mp3",
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Messies Participatiu/Gloria - 05. Domine Deus Rex celestis/voices/Bass.mp3",
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Messies Participatiu/Gloria - 05. Domine Deus Rex celestis/voices/Tenor.mp3",
    "/home/benedikt/thesis/datasets/CANTAMUS_SYNTHESIZED/Cantamus Catalog/Magnificat BWV 243 - 03 Quia respecit/voices/Soprano I.mp3"
]

for x in blacklist:
    all_stems.remove(x)

# extracting original Cantoria recordings for test set
cantoria_originals = []
for x in all_stems:
    #print(x)
    if "Cantoría" in x and not "[" in x:
        cantoria_originals.append(x)


for x in cantoria_originals:
    all_stems.remove(x)


all_stems = [(Path(x), Path(x).parents[0].relative_to(path_to_cantamus), Path(x).stem) for x in all_stems]
all_stems = pd.DataFrame(all_stems, columns = ["full_path", "short_path", "name"])


grouped_by_songs_dict = dict(list(all_stems.groupby(all_stems['short_path'])))

songs_shuffled = shuffle (list (grouped_by_songs_dict.keys()))

split_idx = np.ceil (len (songs_shuffled) * train_valid_split).astype(int)
song_names_train = songs_shuffled[:split_idx]
song_names_validation = songs_shuffled[split_idx:]

df_train = all_stems.loc[all_stems["short_path"].isin(song_names_train)]
df_validation = all_stems.loc[all_stems["short_path"].isin(song_names_validation)]


with open ("train_file_paths.txt", 'w') as handle:
    handle.writelines([str(x) + '\n' for x in df_train['full_path']])

with open ("validation_file_paths.txt", 'w') as handle:
    handle.writelines([str(x) + '\n' for x in df_validation['full_path']])

with open ("test_file_paths.txt", 'w') as handle:
    handle.writelines([str(x) + '\n' for x in cantoria_originals])