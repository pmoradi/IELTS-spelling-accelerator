import os
from tqdm import tqdm
from moviepy.editor import concatenate_audioclips, AudioFileClip
import random
import pandas as pd

def concatenate_audio_moviepy(audio_clip_paths, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    clips = []
    silence = AudioFileClip('./data/silence.mp3')
    for c in audio_clip_paths:
        clips += [AudioFileClip(c)]
        clips += [silence]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)

files = os.listdir('./voices')
random.shuffle(files)


words = []
for f in tqdm(files):
    words += [f[:-4]]

files = [f'./voices/{f}' for f in files if '.mp3' in f]
s = pd.Series(words)
s.to_csv('my_words.csv')

concatenate_audio_moviepy(files, 'test.mp3')

