import modules

# Arguments
NUM_FLUTES = 6
ALLOW_HOLES = True
SONG_PATH = 'data/Seven_Nation_Army.wav'


if __name__ == '__main__':
    generator = modules.FluteGenerator()
    if SONG_PATH.split('.')[-1] == 'mp3':
        generator.mp3_to_wav_converter(SONG_PATH)
    flute_freqs = generator.freq_extractor(SONG_PATH.split('.')[0]+'.wav', first_n_seconds=15, num_freqs=NUM_FLUTES)
    if ALLOW_HOLES:
        pipe_lengths, hole_locations = generator.design_flute(flute_freqs, allow_holes=ALLOW_HOLES)
    else:
        pipe_lengths = generator.design_flute(flute_freqs, allow_holes=ALLOW_HOLES)