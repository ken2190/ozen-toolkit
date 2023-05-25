import os
import glob
import argparse
from pydub import AudioSegment
import colorama
colorama.init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected

def convert_to_wav(file_path):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Add a silent spacer at the beginning
    spacer_milli = 2000
    spacer = AudioSegment.silent(duration=spacer_milli)
    audio = spacer.append(audio, crossfade=0)

    # Export the audio to a WAV file
    base_path, ext = os.path.splitext(file_path)
    output_path = base_path + '.wav'
    audio.export(output_path, format='wav')

    return output_path

def convert_mp3_to_wav(input_folder):
    # Create an output folder for WAV files
    output_folder = os.path.join(input_folder, "output")
    os.makedirs(output_folder, exist_ok=True)

    # Find all MP3 files in the input folder
    mp3_files = glob.glob(os.path.join(input_folder, "*.mp3"))

    for i, mp3_file in enumerate(mp3_files):
        # Print the conversion status using colorama
        print(colorama.Fore.GREEN + 'Converting to WAV...' + colorama.Fore.RESET)

        # Convert MP3 to WAV using the provided function
        wav_file = convert_to_wav(mp3_file)

        # Construct the output WAV file path with a new name
        new_wav_file = os.path.join(output_folder, f"file_{i}.wav")

        # Rename the WAV file
        os.rename(wav_file, new_wav_file)

        # Remove the original MP3 file
        os.remove(mp3_file)

        print(f"Converted {mp3_file} to {new_wav_file}")

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Convert MP3 files to WAV format")

    # Add the --path argument
    parser.add_argument("--path", required=True, help="Input folder path")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Convert MP3 files to WAV and remove the original MP3 files
    convert_mp3_to_wav(args.path)
