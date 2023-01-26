import subprocess
import modules
import argparse

# Arguments
NUM_FLUTES = 6
FIRST_N_SECONDS = 15
ALLOW_HOLES = True
SONG_PATH = "data/Seven_Nation_Army.wav"


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file_path", type=str, default=SONG_PATH, help="File path of song")
    parser.add_argument("-a", "--amount", type=int, default=NUM_FLUTES, help="How many flutes to generate")
    parser.add_argument(
        "-s", "--seconds", type=int, default=FIRST_N_SECONDS, help="How many seconds to use from the song"
    )
    parser.add_argument("--holes", action=argparse.BooleanOptionalAction, default=True, help="Allow holes")
    parser.add_argument("--plot", action=argparse.BooleanOptionalAction, default=False, help="Plot calculations")

    # panpipe params
    parser.add_argument("--sorted", action=argparse.BooleanOptionalAction, default=True, help="sort flutes by length")
    parser.add_argument(
        "-o", "--output", type=str, default="panpipe.stl", help="stl file output path. Default panpipe.stl"
    )
    parser.add_argument("-d", "--dimensions", type=float, default=20, help="the x,z dimensions in mm. Default 20")

    return parser.parse_args()


def convert_results_to_panpipe_format(flutes_lengths, flutes_holes) -> str:
    flutes_in_panpipe_format = []
    for i, flute_length in enumerate(flutes_lengths):
        hole = ":" + str(flutes_holes[i] * 1000) if flutes_holes else ""
        flutes_in_panpipe_format.append(str(flute_length * 1000) + hole)

    return " ".join(flutes_in_panpipe_format)


def initiate_panpipe(flutes: str, sort: bool, output: bool, dimensions: float):
    cwd = "./panpipe"
    blender_file = "flute_with_full_faces.blend"
    script = "panpipe_entrypoint.py"
    sort = "--sorted" if sort else "--no-sorted"

    blender_command = ["blender", "-b", "--log-level", "2", blender_file, "-P", script, "--"]
    panpipe_args = [sort, "-f", flutes, "-o", output, "-d", str(dimensions)]
    result = subprocess.run(
        " ".join(blender_command + panpipe_args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=True
    )
    for line in str(result.stdout).split("\\n"):
        print(line)


if __name__ == "__main__":
    args = parse_args()
    song_path = args.file_path
    amount = args.amount
    holes = args.holes
    first_n_seconds = args.seconds
    plot = args.plot

    # panpip params
    panpipe_sorted = args.sorted
    panpipe_output = args.output
    panpipe_dimensions = args.dimensions

    generator = modules.FluteGenerator()
    if song_path.split(".")[-1] == "mp3":
        generator.mp3_to_wav_converter(song_path)

    flute_freqs = generator.freq_extractor(
        song_path.split(".")[0] + ".wav", first_n_seconds=first_n_seconds, num_freqs=amount, plot_pitches=plot
    )

    if ALLOW_HOLES:
        pipe_lengths, holes_locations = generator.design_flute(flute_freqs, allow_holes=ALLOW_HOLES, plot_flute=plot)
    else:
        holes_locations = []
        pipe_lengths = generator.design_flute(flute_freqs, allow_holes=ALLOW_HOLES, plot_flute=plot)

    flutes_in_panpipe_format = convert_results_to_panpipe_format(pipe_lengths, holes_locations)
    initiate_panpipe(
        flutes=flutes_in_panpipe_format, sort=panpipe_sorted, output=panpipe_output, dimensions=panpipe_dimensions
    )
