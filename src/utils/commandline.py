import argparse
from src.voice.whisper.languages import LANGUAGES, TO_LANGUAGE_CODE
from src.utils.version import __version__

MODEL_NAMES = [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large-v1",
    "large-v2",
    "large-v3",
]


class CommandLine:
    @staticmethod
    def _optional_int(string):
        return None if string == "None" else int(string)

    @staticmethod
    def _str2bool(string):
        str2val = {"true": True, "false": False}
        if string and string.lower() in str2val:
            return str2val[string.lower()]
        else:
            raise ValueError(
                f"Expected one of {set(str2val.keys())}, got {string}")

    @staticmethod
    def _optional_float(string):
        return None if string == "None" else float(string)

    @staticmethod
    def read_command_line():
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # Billy arguments
        parser.add_argument(
            "--verbose",
            type=CommandLine()._str2bool,
            default=False,
            help="Enable verbose logging"
        )

        parser.add_argument(
            "--discord-tts",
            type=CommandLine()._str2bool,
            default=False,
            help="Play text-to-speech through Discord bot rather than computer audio"
        )

        model_args = parser.add_argument_group("Model selection options")

        model_args.add_argument(
            "--model",
            default="medium",
            choices=MODEL_NAMES,
            help="Name of the Whisper model to use",
        )

        model_args.add_argument(
            "--model_directory",
            type=str,
            default=None,
            help="Directory where to find a CTranslate2 Whisper model (e.g. fine-tuned model)",
        )

        caching_args = parser.add_argument_group(
            "Model caching control options"
        )

        caching_args.add_argument(
            "--model_dir",
            type=str,
            default=None,
            help="The path to save model files; uses ~/.cache/huggingface/ by default",
        )

        caching_args.add_argument(
            "--local_files_only",
            type=CommandLine()._str2bool,
            default=False,
            help="Use models in cache without connecting to Internet to check if there are newer versions",
        )

        computing_args = parser.add_argument_group(
            "Computing configuration options"
        )

        computing_args.add_argument(
            "--device",
            choices=[
                "auto",
                "cpu",
                "cuda",
            ],
            default="auto",
            help="Device to use for Whisper inference",
        )

        computing_args.add_argument(
            "--threads",
            type=CommandLine()._optional_int,
            default=0,
            help="Number of threads used for CPU inference",
        )

        computing_args.add_argument(
            "--device_index",
            type=int,
            default=0,
            help="Device ID where to place this model on",
        )

        computing_args.add_argument(
            "--compute_type",
            choices=[
                "default",
                "auto",
                "int8",
                "int8_float16",
                "int8_bfloat16",
                "int8_float32",
                "int16",
                "float16",
                "float32",
                "bfloat16",
            ],
            default="auto",
            help="Type of quantization to use (see https://opennmt.net/CTranslate2/quantization.html)",
        )

        algorithm_args = parser.add_argument_group(
            "Algorithm execution options"
        )

        algorithm_args.add_argument(
            "--language",
            type=str,
            default=None,
            choices=sorted(LANGUAGES.keys())
            + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
            help="Language spoken in the audio, specify None to perform language detection",
        )

        algorithm_args.add_argument(
            "--temperature",
            type=float,
            default=0,
            help="Temperature to use for sampling",
        )

        algorithm_args.add_argument(
            "--temperature_increment_on_fallback",
            type=CommandLine()._optional_float,
            default=0.2,
            help="Temperature to increase when falling back when the decoding fails to meet either of the thresholds below",
        )

        algorithm_args.add_argument(
            "--prompt_reset_on_temperature",
            type=float,
            default=0.5,
            help="Resets prompt if temperature is above this value. Arg has effect only if condition_on_previous_text is True",
        )

        algorithm_args.add_argument(
            "--best_of",
            type=CommandLine()._optional_int,
            default=5,
            help="Number of candidates when sampling with non-zero temperature",
        )

        algorithm_args.add_argument(
            "--beam_size",
            type=CommandLine()._optional_int,
            default=5,
            help="Number of beams in beam search, only applicable when temperature is zero",
        )

        algorithm_args.add_argument(
            "--patience",
            type=float,
            default=1.0,
            help="Optional patience value to use in beam decoding, as in https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to conventional beam search",
        )

        algorithm_args.add_argument(
            "--length_penalty",
            type=float,
            default=1.0,
            help="Optional token length penalty coefficient (alpha) as in https://arxiv.org/abs/1609.08144, uses simple length normalization by default",
        )

        algorithm_args.add_argument(
            "--suppress_blank",
            type=CommandLine()._str2bool,
            default="True",
            help="Suppress blank outputs at the beginning of the sampling",
        )

        algorithm_args.add_argument(
            "--suppress_tokens",
            type=str,
            default="-1",
            help="Comma-separated list of token ids to suppress during sampling; '-1' will suppress most special characters except common punctuations",
        )

        algorithm_args.add_argument(
            "--initial_prompt",
            type=str,
            default=None,
            help="Optional text to provide as a prompt for the first window.",
        )

        algorithm_args.add_argument(
            "--condition_on_previous_text",
            type=CommandLine()._str2bool,
            default=True,
            help="If True, provide the previous output of the model as a prompt for the next window; disabling may make the text inconsistent across windows, but the model becomes less prone to getting stuck in a failure loop",
        )

        algorithm_args.add_argument(
            "--compression_ratio_threshold",
            type=CommandLine()._optional_float,
            default=2.4,
            help="If the gzip compression ratio is higher than this value, treat the decoding as failed",
        )

        algorithm_args.add_argument(
            "--logprob_threshold",
            type=CommandLine()._optional_float,
            default=-1.0,
            help="If the average log probability is lower than this value, treat the decoding as failed",
        )

        algorithm_args.add_argument(
            "--no_speech_threshold",
            type=CommandLine()._optional_float,
            default=0.6,
            help="If the probability of the <|nospeech|> token is higher than this value AND the decoding has failed due to `logprob_threshold`, consider the segment as silence",
        )

        algorithm_args.add_argument(
            "--word_timestamps",
            type=CommandLine()._str2bool,
            default=False,
            help="(experimental) extract word-level timestamps and refine the results based on them",
        )

        algorithm_args.add_argument(
            "--prepend_punctuations",
            type=str,
            default="\"'“¿([{-",
            help="If word_timestamps is True, merge these punctuation symbols with the next word",
        )

        algorithm_args.add_argument(
            "--append_punctuations",
            type=str,
            default="\"'.。,，!！?？:：”)]}、",
            help="If word_timestamps is True, merge these punctuation symbols with the previous word",
        )

        algorithm_args.add_argument(
            "--repetition_penalty",
            type=float,
            default=1.0,
            help="Penalty applied to the score of previously generated tokens (set > 1 to penalize)",
        )

        algorithm_args.add_argument(
            "--no_repeat_ngram_size",
            type=int,
            default=0,
            help="Prevent repetitions of ngrams with this size (set 0 to disable)",
        )

        vad_args = parser.add_argument_group("VAD filter arguments")

        vad_args.add_argument(
            "--vad_filter",
            type=CommandLine()._str2bool,
            default=False,
            help="Enable the voice activity detection (VAD) to filter out parts of the audio without speech. This step is using the Silero VAD model https://github.com/snakers4/silero-vad.",
        )

        vad_args.add_argument(
            "--vad_threshold",
            type=float,
            default=None,
            help="When `vad_filter` is enabled, probabilities above this value are considered as speech.",
        )

        vad_args.add_argument(
            "--vad_min_speech_duration_ms",
            type=int,
            default=None,
            help="When `vad_filter` is enabled, final speech chunks shorter min_speech_duration_ms are thrown out.",
        )

        vad_args.add_argument(
            "--vad_max_speech_duration_s",
            type=int,
            default=None,
            help="When `vad_filter` is enabled, Maximum duration of speech chunks in seconds. Longer will be split at the timestamp of the last silence.",
        )

        vad_args.add_argument(
            "--vad_min_silence_duration_ms",
            type=int,
            default=None,
            help="When `vad_filter` is enabled, in the end of each speech chunk time to wait before separating it.",
        )

        parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s {version}".format(version=__version__),
            help="Show program's version number and exit",
        )

        live_args = parser.add_argument_group("Live transcribe options")

        live_args.add_argument(
            "--live_volume_threshold",
            type=float,
            default=0.01,
            help="Minimum volume threshold to activate listening in live transcribe mode",
        )

        live_args.add_argument(
            "--live_input_device",
            type=int,
            default=None,
            help="Set live stream input device ID (see python -m sounddevice for a list)",
        )

        return parser.parse_args()
