import subprocess


class LocalAudioPlayer:
    def __init__(self):
        pass

    def play_stream(self, url):
        command = [
            "ffmpeg",
            "-i", url,
            "-f", "wav",  # Force format to wav for compatibility
            "-acodec", "pcm_s16le",  # Audio codec
            "-ar", "44100",
            "-ac", "2",
            "-",  # Output to stdout
        ]

        # Play audio with ffplay (part of ffmpeg)
        play_command = ["ffplay", "-nodisp", "-autoexit", "-"]

        # Set up the subprocess to hide the output
        process_ffmpeg = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        process_ffplay = subprocess.Popen(
            play_command, stdin=process_ffmpeg.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        process_ffplay.wait()
