import asyncio
import datetime
import os
import sys
import warnings
from typing import List, Union

import numpy as np

from src.utils.config import CLIArgs
from src.voice.whisper.languages import from_language_to_iso_code
from src.voice.whisper.live import Live
from src.voice.whisper.transcribe import TranscriptionOptions


def get_diarization(audio, diarize_model, verbose):
    diarization_output = {}
    for audio_path in audio:
        if verbose and len(audio) > 1:
            print(f"\nFile: '{audio_path}' (diarization)")

        start_time = datetime.datetime.now()
        diarize_segments = diarize_model.run_model(audio_path)
        diarization_output[audio_path] = diarize_segments
        if verbose:
            print(
                f"Time used for diarization: {datetime.datetime.now() - start_time}")

    diarize_model.unload_model()
    return diarization_output


def get_transcription_options():
    temperature = CLIArgs.temperature

    if (increment := CLIArgs.temperature_increment_on_fallback) is not None:
        temperature = tuple(np.arange(temperature, 1.0 + 1e-6, increment))
    else:
        temperature = [temperature]

    suppress_tokens: str = CLIArgs.suppress_tokens
    suppress_tokens = [int(t) for t in suppress_tokens.split(",")]

    return TranscriptionOptions(
        beam_size=CLIArgs.beam_size,
        best_of=CLIArgs.best_of,
        patience=CLIArgs.patience,
        length_penalty=CLIArgs.length_penalty,
        repetition_penalty=CLIArgs.repetition_penalty,
        no_repeat_ngram_size=CLIArgs.no_repeat_ngram_size,
        log_prob_threshold=CLIArgs.logprob_threshold,
        no_speech_threshold=CLIArgs.no_speech_threshold,
        compression_ratio_threshold=CLIArgs.compression_ratio_threshold,
        condition_on_previous_text=CLIArgs.condition_on_previous_text,
        temperature=temperature,
        prompt_reset_on_temperature=CLIArgs.prompt_reset_on_temperature,
        initial_prompt=CLIArgs.initial_prompt,
        suppress_blank=CLIArgs.suppress_blank,
        suppress_tokens=suppress_tokens,
        word_timestamps=CLIArgs.word_timestamps,
        prepend_punctuations=CLIArgs.prepend_punctuations,
        append_punctuations=CLIArgs.append_punctuations,
        print_colors=CLIArgs.print_colors,
        vad_filter=CLIArgs.vad_filter,
        vad_threshold=CLIArgs.vad_threshold,
        vad_min_speech_duration_ms=CLIArgs.vad_min_speech_duration_ms,
        vad_max_speech_duration_s=CLIArgs.vad_max_speech_duration_s,
        vad_min_silence_duration_ms=CLIArgs.vad_min_silence_duration_ms,
    )


def get_language(language, model_directory, model):
    language = from_language_to_iso_code(language)

    if (
        not model_directory
        and model.endswith(".en")
        and language not in {"en", "English"}
    ):
        if language is not None:
            warnings.warn(
                f"{model} is an English-only model but receipted '{language}'; using English instead."
            )
        language = "en"

    return language


class LiveTranscribe:
    def transcribe(self):
        live = Live(
            self.model_dir,
            self.cache_directory,
            self.local_files_only,
            self.language,
            self.threads,
            self.device,
            self.device_index,
            self.compute_type,
            self.verbose,
            self.live_volume_threshold,
            self.live_input_device,
            self.options,
        )

        live.on_transcription_callback = self.on_transcription_callback

        live.inference()

    def __init__(self, on_transcription_callback=None):
        self.on_transcription_callback = on_transcription_callback

        self.model: str = CLIArgs.model
        self.threads: int = CLIArgs.threads
        self.language: str = CLIArgs.language
        self.device: str = CLIArgs.device
        self.compute_type: str = CLIArgs.compute_type
        self.verbose: bool = CLIArgs.verbose
        self.model_directory: str = CLIArgs.model_directory
        self.cache_directory: str = CLIArgs.model_dir
        self.device_index: Union[int, List[int]] = CLIArgs.device_index
        self.live_transcribe: bool = CLIArgs.live_transcribe
        self.local_files_only: bool = CLIArgs.local_files_only
        self.live_volume_threshold: float = CLIArgs.live_volume_threshold
        self.live_input_device: int = CLIArgs.live_input_device

        self.language = get_language(
            self.language, self.model_directory, self.model)
        self.options = get_transcription_options()

        if self.live_transcribe and not Live.is_available():
            Live.force_not_available_exception()

        if self.verbose and not self.language:
            if self.live_transcribe:
                print(
                    "Consider specifying the language using `--language`. It improves significantly prediction in live transcription."
                )
            else:
                print(
                    "Detecting language using up to the first 30 seconds. Use `--language` to specify the language"
                )

        if self.model_directory:
            model_filename = os.path.join(self.model_directory, "model.bin")
            if not os.path.exists(model_filename):
                sys.stderr.write(
                    f"Model file '{model_filename}' does not exists\n")
                return
            self.model_dir = self.model_directory
        else:
            self.model_dir = self.model
