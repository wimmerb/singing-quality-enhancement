import os
import glob
from pathlib import Path

import librosa
import numpy as np
# import sounddevice as sd
import soundfile as sf
import tqdm
from random import choice

# #==========CHANGE HERE==========
# path = "ACE"
# sr = 48000
# max_len = 60*sr #60 seconds are sufficient
# copy_all_channels = True
# #==========CHANGE HERE==========

# #==========CHANGE HERE==========
# path = "noise_files"
# sr = 44100
# max_len = 60*sr #60 seconds are sufficient
# copy_all_channels = True
# #==========CHANGE HERE==========

#==========CHANGE HERE==========
path = "/home/benedikt/thesis/TRAIN_EVALUATION_DATA/TROMPA_REHEARSALS/TROMPA_REHEARSALS_WAV"
sr = 16000
max_len = 60*sr
copy_all_channels = True
#==========CHANGE HERE==========




for filename in tqdm.tqdm(list (Path(path).rglob('*.wav')) + list (Path(path).rglob('*.flac')) + list (Path(path).rglob('*.ogg'))):
    # load file
    audio_arr, sr = librosa.load (filename, sr, mono = False)

    # create filename for directory to clone to e.g. 'ACE/bla/bla' -> 'ACE_mono_clone/bla/bla'
    filename_new = Path(*([f"{path}_mono_clone"] + list(filename.parts[1:])))
    #print (filename_new.parts)

    # creating directory needed to write file to
    if not os.path.exists(Path(*filename_new.parts[:-1])):
        os.makedirs (Path(*filename_new.parts[:-1]))

    # if non-mono -> make a mono file for each channel of audio
    if audio_arr.ndim > 1:
        if copy_all_channels:
            channels = range (audio_arr.shape[0])
        else:
            channels = [choice (range (audio_arr.shape[0]))]
        #print (">1")
        for audio_arr_idx in channels:
            # if (audio_arr.shape[1] > max_len):
            #     print ("too long", filename)
            audio_arr_new = audio_arr[audio_arr_idx, :max_len]
            basename = os.path.splitext(filename_new.parts[-1])[0]
            basename += f"_c{audio_arr_idx}.wav" if copy_all_channels else f".wav"
            filename_w_channel = Path(*(list (filename_new.parts[:-1]) + [basename]))
        #    print (filename_w_channel)
            sf.write (filename_w_channel, audio_arr_new, sr, subtype = 'PCM_16', format = 'WAV')

    # else -> just print it out to new driectory
    else:
        #print ("=1")
        # if (audio_arr.shape[0] > max_len):
        #     print ("too long", filename)
        audio_arr_new = audio_arr[:max_len]
        basename = os.path.splitext(filename_new.parts[-1])[0]
        basename += f".wav"
        filename_full_wav = Path(*(list (filename_new.parts[:-1]) + [basename]))
        #print (filename_full_wav)
        sf.write (filename_full_wav, audio_arr_new, sr, subtype = 'PCM_16', format = 'WAV')

